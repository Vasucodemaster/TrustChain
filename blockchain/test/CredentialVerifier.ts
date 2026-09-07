import { expect } from "chai";
import { network } from "hardhat";
import fs from "fs";

describe("TrustChain CredentialVerifier", function () {
  it("should verify the generated ZK proof", async function () {
    const { ethers } = await network.create();

    const verifier = await ethers.deployContract("Groth16Verifier");
    await verifier.waitForDeployment();

    const proof = JSON.parse(
      fs.readFileSync("circuits/setup/proof.json", "utf8")
    );

    const publicSignals = JSON.parse(
      fs.readFileSync("circuits/setup/public.json", "utf8")
    );

    const pA = proof.pi_a.slice(0, 2);

    const pB = proof.pi_b
      .slice(0, 2)
      .map((pair: string[]) => [pair[1], pair[0]]);

    const pC = proof.pi_c.slice(0, 2);

    const result = await verifier.verifyProof(
      pA,
      pB,
      pC,
      publicSignals
    );

    expect(result).to.equal(true);
  });
});
