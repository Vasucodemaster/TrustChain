import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  const ReputationSBT =
    await ethers.getContractFactory("ReputationSBT");

  const reputation = await ReputationSBT.deploy();

  await reputation.waitForDeployment();

  console.log(
    "ReputationSBT deployed to:",
    await reputation.getAddress()
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
