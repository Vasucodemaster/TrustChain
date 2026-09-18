import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

  const ReputationSBT = await ethers.getContractFactory("ReputationSBT");

  const reputation = ReputationSBT.attach(contractAddress);

  const [admin, contributor] = await ethers.getSigners();

  console.log("Admin:", admin.address);
  console.log("Contributor:", contributor.address);

  console.log("\nMinting reputation...");

  const tx = await reputation.mintReputation(
    1,
    contributor.address,
    85
  );

  await tx.wait();

  console.log("Reputation minted.");

  const result = await reputation.getReputation(1);

  console.log("\n===== F6 REPUTATION =====");
  console.log("Contributor ID:", 1);
  console.log("Score:", result[0].toString());
  console.log("Updated At:", result[1].toString());
  console.log("Owner:", result[2]);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
