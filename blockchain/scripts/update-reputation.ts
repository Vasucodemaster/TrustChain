import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  const contractAddress =
    "0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9";

  const ReputationSBT =
    await ethers.getContractFactory("ReputationSBT");

  const reputation =
    ReputationSBT.attach(contractAddress);

  console.log("Updating Contributor 1 reputation...");

  const tx = await reputation.updateReputation(1, 92);

  await tx.wait();

  const result = await reputation.getReputation(1);

  console.log("\n===== UPDATED F6 REPUTATION =====");
  console.log("Contributor ID:", 1);
  console.log("New Score:", result[0].toString());
  console.log("Updated At:", result[1].toString());
  console.log("Owner:", result[2]);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
