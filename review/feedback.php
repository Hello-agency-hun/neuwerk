<?php
/**
 * Visszajelzés-gyűjtő a review-buildhez.
 *
 * CSAK a bemutató-változat része. Az éles csomagban NINCS benne -- ott a
 * site tiszta statikus HTML/CSS/JS, szerveroldal nélkül.
 *
 * Egyetlen dolgot csinál: hozzáfűz egy bejegyzést a feedback/comments.json
 * fájlhoz. Nem olvas be semmilyen útvonalat a kérésből, nem ír máshova,
 * és nem futtat semmit.
 *
 * GET  -> a teljes JSON visszaadása (letöltéshez)
 * POST -> egy új bejegyzés hozzáfűzése
 */

declare(strict_types=1);

const DATA_DIR   = __DIR__ . '/feedback';
const DATA_FILE  = DATA_DIR . '/comments.json';
const MAX_BYTES  = 8000;     // egy bejegyzés maximális mérete
const MAX_ENTRIES = 2000;    // fölötte nem fűzünk hozzá többet

/* Ha bármi váratlan fatal errort dob, a kliens üres választ kapna és csak
   annyit tudna mondani, hogy "nem sikerült". Ez a védőháló legalább
   megmondja, mi történt. */
register_shutdown_function(static function (): void {
    $e = error_get_last();
    if ($e && in_array($e['type'], [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR], true)) {
        if (!headers_sent()) {
            http_response_code(500);
            header('Content-Type: application/json; charset=utf-8');
        }
        echo json_encode([
            'ok' => false,
            'error' => 'Szerveroldali hiba: ' . $e['message'],
        ], JSON_UNESCAPED_UNICODE);
    }
});

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

/** UTF-8 biztos vágás mbstring NÉLKÜL is.
 *  A shared hostingokon általában van mbstring, de nem mindenhol -- és ha
 *  hiányzik, az mb_substr fatal errort dob, a válasz üres lesz, a widget
 *  pedig csak annyit tud mondani, hogy "nem sikerült". Ezt mértem is.
 *  A /u módosítós regex a PCRE-vel mindenhol elérhető. */
function u_trunc(string $s, int $max): string {
    if (function_exists('mb_substr')) {
        return mb_substr($s, 0, $max, 'UTF-8');
    }
    if (preg_match('/^.{0,' . $max . '}/us', $s, $m)) {
        return $m[0];
    }
    return substr($s, 0, $max);
}

function fail(int $code, string $msg): void {
    http_response_code($code);
    echo json_encode(['ok' => false, 'error' => $msg], JSON_UNESCAPED_UNICODE);
    exit;
}

function load(): array {
    if (!is_file(DATA_FILE)) return [];
    $raw = file_get_contents(DATA_FILE);
    if ($raw === false || $raw === '') return [];
    $data = json_decode($raw, true);
    return is_array($data) ? $data : [];
}

// --- Letöltés ---------------------------------------------------------
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $entries = load();
    if (isset($_GET['download'])) {
        header('Content-Disposition: attachment; filename="neuwerk-feedback.json"');
    }
    echo json_encode(
        ['ok' => true, 'count' => count($entries), 'entries' => $entries],
        JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT
    );
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    fail(405, 'Csak GET vagy POST.');
}

// --- Bejegyzés hozzáfűzése -------------------------------------------
$raw = file_get_contents('php://input');
if ($raw === false || strlen($raw) > MAX_BYTES) {
    fail(413, 'Túl nagy vagy olvashatatlan kérés.');
}

$in = json_decode($raw, true);
if (!is_array($in)) fail(400, 'Érvénytelen JSON.');

// Csak a saját mezőinket vesszük át, semmi mást. A page a böngészőből jön,
// de nem használjuk fájlműveletre -- csak szövegként tároljuk.
$clean = static function (?string $v, int $max): string {
    $v = trim((string)$v);
    $v = str_replace(["\0", "\r"], '', $v);
    return u_trunc($v, $max);
};

$comment = $clean($in['comment'] ?? '', 4000);
if ($comment === '') fail(400, 'A megjegyzés nem lehet üres.');

$entry = [
    'id'       => bin2hex(random_bytes(6)),
    'ts'       => gmdate('c'),
    'page'     => $clean($in['page'] ?? '', 200),
    'title'    => $clean($in['title'] ?? '', 300),
    'section'  => $clean($in['section'] ?? '', 120),
    'category' => $clean($in['category'] ?? '', 60),
    'author'   => $clean($in['author'] ?? '', 120),
    'comment'  => $comment,
    'viewport' => $clean($in['viewport'] ?? '', 40),
];

if (!is_dir(DATA_DIR) && !@mkdir(DATA_DIR, 0775, true) && !is_dir(DATA_DIR)) {
    fail(500, 'Nem tudom létrehozni a feedback mappát. Adj rá írási jogot.');
}

$fh = @fopen(DATA_FILE, 'c+');
if ($fh === false) fail(500, 'Nem tudom megnyitni a comments.json fájlt. Adj rá írási jogot.');

if (!flock($fh, LOCK_EX)) { fclose($fh); fail(500, 'A fájl zárolása nem sikerült.'); }

$size = filesize(DATA_FILE) ?: 0;
$existing = $size > 0 ? (json_decode((string)fread($fh, $size), true) ?: []) : [];
if (!is_array($existing)) $existing = [];

if (count($existing) >= MAX_ENTRIES) {
    flock($fh, LOCK_UN); fclose($fh);
    fail(507, 'Betelt a visszajelzés-napló.');
}

$existing[] = $entry;

rewind($fh);
ftruncate($fh, 0);
fwrite($fh, json_encode($existing, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
fflush($fh);
flock($fh, LOCK_UN);
fclose($fh);

echo json_encode(['ok' => true, 'id' => $entry['id'], 'count' => count($existing)], JSON_UNESCAPED_UNICODE);
