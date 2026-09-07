import fs from "fs";
import * as snarkjs from "snarkjs";

const credentialScore = Number(process.argv[2]);
const minimumScore = Number(process.argv[3]);

if (
  !Number.isInteger(credentialScore) ||
  !Number.isInteger(minimumScore) ||
  credentialScore < 0 ||
  credentialScore > 255 ||
  minimumScore < 0 ||
  minimumScore > 255
) {
  console.error("Scores must be integers between 0 and 255.");
  process.exit(1);
}

const basePath = new URL("./circuits/", import.meta.url);
const setupPath = new URL("./circuits/setup/", import.meta.url);

const wasmPath = new URL(
  "./credential_js/credential.wasm",
  basePath
);

const zkeyPath = new URL(
  "./credential_final.zkey",
  setupPath
);

const verificationKey = JSON.parse(
  fs.readFileSync(
    new URL("verification_key.json", setupPath),
    "utf8"
  )
);

const { proof, publicSignals } =
  await snarkjs.groth16.fullProve(
    {
      credential_score: credentialScore,
      minimum_score: minimumScore
    },
    wasmPath.pathname,
    zkeyPath.pathname
  );

const verified = await snarkjs.groth16.verify(
  verificationKey,
  publicSignals,
  proof
);

console.log(
  JSON.stringify({
    verified: verified,
    publicSignals: publicSignals
  })
);

process.exit(0);
