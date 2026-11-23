// News image entry: deliver the pre-rendered front page.
//
// Node 22, standard library only, no network. Reads entry.png from the same
// directory, refuses anything that is not a whole 1024x1024 PNG of at most
// 1 MiB, then writes the identical bytes to
// $MAKEFUN_OUTPUT_DIR/entry.png (default /output) and proves the copy by
// reading it back and comparing bytes.

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const LIMIT = 1024 * 1024;
const SIDE = 1024;

function fail(reason: string): never {
  console.error(`error: ${reason}`);
  process.exit(1);
}

function dimsOf(buf: Buffer): [number, number] {
  // IHDR: width and height are the first two big-endian u32 after the
  // 8-byte signature, the 4-byte length and the 4-byte "IHDR" tag.
  if (buf.length < 33 || buf.subarray(12, 16).toString("ascii") !== "IHDR") {
    fail("missing IHDR chunk");
  }
  return [buf.readUInt32BE(16), buf.readUInt32BE(20)];
}

function tailOk(buf: Buffer): boolean {
  // A whole PNG ends with a 12-byte IEND chunk: length 0, tag IEND.
  if (buf.length < 12) return false;
  const tail = buf.subarray(buf.length - 12);
  return tail.readUInt32BE(0) === 0 && tail.subarray(4, 8).toString("ascii") === "IEND";
}

async function run(): Promise<void> {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, "entry.png");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const dest = join(outDir, "entry.png");

  let bytes: Buffer;
  try {
    bytes = await readFile(source);
  } catch {
    fail(`cannot read ${source}`);
  }

  if (bytes.length > LIMIT) fail(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
  if (!bytes.subarray(0, 8).equals(SIGNATURE)) fail("entry.png is not a PNG");
  const [w, h] = dimsOf(bytes);
  if (w !== SIDE || h !== SIDE) fail(`entry.png is ${w}x${h}, want 1024x1024`);
  if (!tailOk(bytes)) fail("entry.png is truncated (no IEND chunk)");

  await mkdir(outDir, { recursive: true });
  await writeFile(dest, bytes);

  const back = await readFile(dest);
  if (!back.equals(bytes)) fail("copy check failed: output differs from entry.png");
  console.log(`wrote ${dest} (${bytes.length} bytes, 1024x1024 PNG, verified identical)`);
}

run().catch((err: unknown) => fail(err instanceof Error ? err.message : String(err)));
