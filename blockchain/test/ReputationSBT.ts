import { expect } from "chai";
import { network } from "hardhat";

describe("ReputationSBT", function () {

  it("should mint and read a reputation", async function () {
    const { ethers } = await network.connect();

    const [admin, contributor] = await ethers.getSigners();

    const ReputationSBT =
      await ethers.getContractFactory("ReputationSBT");

    const reputation = await ReputationSBT.deploy();

    await reputation.waitForDeployment();

    await reputation.mintReputation(
      1,
      contributor.address,
      85
    );

    const result = await reputation.getReputation(1);

    expect(result[0]).to.equal(85);
    expect(result[2]).to.equal(contributor.address);
  });


  it("should dynamically update reputation", async function () {
    const { ethers } = await network.connect();

    const [admin, contributor] = await ethers.getSigners();

    const ReputationSBT =
      await ethers.getContractFactory("ReputationSBT");

    const reputation = await ReputationSBT.deploy();

    await reputation.waitForDeployment();

    await reputation.mintReputation(
      1,
      contributor.address,
      70
    );

    let result = await reputation.getReputation(1);

    expect(result[0]).to.equal(70);

    await reputation.updateReputation(
      1,
      90
    );

    result = await reputation.getReputation(1);

    expect(result[0]).to.equal(90);
  });


  it("should prevent unauthorized reputation updates", async function () {
    const { ethers } = await network.connect();

    const [admin, contributor, attacker] =
      await ethers.getSigners();

    const ReputationSBT =
      await ethers.getContractFactory("ReputationSBT");

    const reputation = await ReputationSBT.deploy();

    await reputation.waitForDeployment();

    await reputation.mintReputation(
      1,
      contributor.address,
      80
    );

    await expect(
      reputation
        .connect(attacker)
        .updateReputation(1, 100)
    ).to.be.revertedWith(
      "Only admin can perform this action"
    );
  });

});
