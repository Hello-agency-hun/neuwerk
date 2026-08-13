<?php
/**
 * Visszajelzés-gyűjtő a review-buildhez.
 *
 * CSAK a bemutató-változat része. Az éles csomagban NINCS benne -- ott a
 * site tiszta statikus HTML/CSS/JS, szerveroldal nélkül.
 *
 * Minden megjegyzés KÜLÖN JSON fájlba kerül a feedback/ mappában:
 *     feedback/2026-08-12T09-14-33Z__index-html__a1b2c3d4e5f6.json
 *
 * Miért külön fájl és nem egy közös:
 *   - nincs zárolási versengés, ha többen egyszerre kommentelnek
 *   - egy elrontott írás nem viszi el az összes korábbi megjegyzést
 *   - a fájlnévben ott az oldal és az időpont, tehát rendezni és szűrni
 *     lehet anélkül, hogy bármit megnyitnánk
 *
 * Végpontok:
 *   POST                -> egy új megjegyzés mentése külön fájlba
 *   GET                 -> összesített JSON (böngészőben olvasható)
 *   GET ?download=1     -> ugyanaz, letöltésként
 *   GET ?zip=1          -> az összes külön fájl egy ZIP-ben (ha van ZipArchive)
 *   GET ?stat=1         -> csak darabszám és oldalankénti bontás
 */

declare(strict_types=1);

const DATA_DIR    = __DIR__ . '/feedback';
const MAX_BYTES   = 8000;    // egy kérés maximális mérete
const MAX_ENTRIES = 5000;    // fölötte nem fogadunk többet

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

header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

/** UTF-8 biztos vágás mbstring NÉLKÜL is.
 *  A shared hostingokon általában van mbstring, de nem mindenhol -- és ha
 *  hiányzik, az mb_substr fatal errort dob, a válasz üres lesz, a widget
 *  pedig csak annyit tud mondani, hogy "nem sikerült". Ezt mértük is.
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

function json_out(array $data, int $code = 200): void {
    if (!headers_sent()) {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
    }
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

function fail(int $code, string $msg): void {
    json_out(['ok' => false, 'error' => $msg], $code);
}

/** A feedback mappa összes megjegyzése, időrendben. */
function all_entries(): array {
    if (!is_dir(DATA_DIR)) return [];
    $files = glob(DATA_DIR . '/*.json') ?: [];
    sort($files, SORT_STRING);          // a fájlnév ISO időbélyeggel kezdődik
    $out = [];
    foreach ($files as $f) {
        $raw = @file_get_contents($f);
        if ($raw === false || $raw === '') continue;
        $d = json_decode($raw, true);
        if (is_array($d)) {
            $d['_file'] = basename($f);
            $out[] = $d;
        }
    }
    return $out;
}

/** Fájlnévbe biztonságos szelet: csak betű, szám, kötőjel. */
function slug(string $s, int $max = 40): string {
    $s = strtolower($s);
    $s = preg_replace('/[^a-z0-9]+/', '-', $s) ?? '';
    $s = trim($s, '-');
    return $s === '' ? 'ismeretlen' : substr($s, 0, $max);
}

// =====================================================================
//  GET
// =====================================================================
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $entries = all_entries();

    // Csak statisztika: ki mit mondott, hányszor melyik oldalra
    if (isset($_GET['stat'])) {
        $byPage = [];
        $byCat = [];
        $byAuthor = [];
        foreach ($entries as $e) {
            $p = $e['page'] ?? '?';
            $c = $e['category'] ?? '?';
            $a = ($e['author'] ?? '') !== '' ? $e['author'] : '(névtelen)';
            $byPage[$p] = ($byPage[$p] ?? 0) + 1;
            $byCat[$c] = ($byCat[$c] ?? 0) + 1;
            $byAuthor[$a] = ($byAuthor[$a] ?? 0) + 1;
        }
        arsort($byPage); arsort($byCat); arsort($byAuthor);
        json_out([
            'ok' => true,
            'count' => count($entries),
            'oldalankent' => $byPage,
            'kategoriankent' => $byCat,
            'szerzonkent' => $byAuthor,
        ]);
    }

    // Az összes külön fájl egy ZIP-ben
    if (isset($_GET['zip'])) {
        if (!class_exists('ZipArchive')) {
            fail(501, 'Ezen a tárhelyen nincs ZipArchive. Használd a ?download=1 összesített JSON-t.');
        }
        $tmp = tempnam(sys_get_temp_dir(), 'nwfb');
        if ($tmp === false) fail(500, 'Nem tudok ideiglenes fájlt létrehozni.');
        $zip = new ZipArchive();
        if ($zip->open($tmp, ZipArchive::OVERWRITE) !== true) fail(500, 'Nem tudom megnyitni a ZIP-et.');
        foreach (glob(DATA_DIR . '/*.json') ?: [] as $f) {
            $zip->addFile($f, basename($f));
        }
        $zip->close();
        if (!headers_sent()) {
            header('Content-Type: application/zip');
            header('Content-Disposition: attachment; filename="neuwerk-feedback.zip"');
            header('Content-Length: ' . (string)filesize($tmp));
        }
        readfile($tmp);
        @unlink($tmp);
        exit;
    }

    if (isset($_GET['download']) && !headers_sent()) {
        header('Content-Disposition: attachment; filename="neuwerk-feedback.json"');
    }
    json_out(['ok' => true, 'count' => count($entries), 'entries' => $entries]);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    fail(405, 'Csak GET vagy POST.');
}

// =====================================================================
//  POST — egy megjegyzés, egy fájl
// =====================================================================
$raw = file_get_contents('php://input');
if ($raw === false || strlen($raw) > MAX_BYTES) {
    fail(413, 'Túl nagy vagy olvashatatlan kérés.');
}

$in = json_decode($raw, true);
if (!is_array($in)) fail(400, 'Érvénytelen JSON.');

// Csak a saját mezőinket vesszük át, semmi mást. A page a böngészőből jön;
// fájlnévbe CSAK a slug()-olt változata kerül, soha a nyers érték.
$clean = static function ($v, int $max): string {
    $v = trim((string)$v);
    $v = str_replace(["\0", "\r"], '', $v);
    return u_trunc($v, $max);
};

$comment = $clean($in['comment'] ?? '', 4000);
if ($comment === '') fail(400, 'A megjegyzés nem lehet üres.');

if (!is_dir(DATA_DIR) && !@mkdir(DATA_DIR, 0775, true) && !is_dir(DATA_DIR)) {
    fail(500, 'Nem tudom létrehozni a feedback mappát. Adj rá írási jogot.');
}

if (count(glob(DATA_DIR . '/*.json') ?: []) >= MAX_ENTRIES) {
    fail(507, 'Betelt a visszajelzés-napló.');
}

$id   = bin2hex(random_bytes(6));
$page = $clean($in['page'] ?? '', 200);

$entry = [
    'id'       => $id,
    'ts'       => gmdate('c'),
    'page'     => $page,
    'title'    => $clean($in['title'] ?? '', 300),
    'section'  => $clean($in['section'] ?? '', 120),
    'category' => $clean($in['category'] ?? '', 60),
    'author'   => $clean($in['author'] ?? '', 120),
    'comment'  => $comment,
    'viewport' => $clean($in['viewport'] ?? '', 40),
    // Melyik bemutato-kor. A build irja a lapba (window.NWR_ROUND), igy
    // ket kor megjegyzesei akkor is szetvalogathatok, ha valaki ugyanabba
    // a konyvtarba tolti fel oket.
    'round'    => $clean($in['round'] ?? '', 60),
];

// A fájlnév rendezhető és beszédes: időbélyeg + oldal + azonosító.
$name = sprintf('%s__%s__%s.json', gmdate('Y-m-d\TH-i-s\Z'), slug($page), $id);
$path = DATA_DIR . '/' . $name;

$written = @file_put_contents(
    $path,
    json_encode($entry, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT),
    LOCK_EX
);
if ($written === false) {
    fail(500, 'Nem tudom kiírni a megjegyzést. Adj írási jogot a feedback mappára.');
}

json_out([
    'ok' => true,
    'id' => $id,
    'file' => $name,
    'count' => count(glob(DATA_DIR . '/*.json') ?: []),
]);
