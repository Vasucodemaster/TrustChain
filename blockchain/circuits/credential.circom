pragma circom 2.2.0;

include "circomlib/circuits/comparators.circom";

template CredentialVerification() {

    // Private: actual reputation score
    signal input credential_score;

    // Public: minimum score required
    signal input minimum_score;

    // Public output
    signal output valid;

    // Check whether credential_score < minimum_score
    component comparator = LessThan(8);

    comparator.in[0] <== credential_score;
    comparator.in[1] <== minimum_score;

    // If credential_score is NOT less than minimum_score,
    // the credential is valid.
    valid <== 1 - comparator.out;
}

component main {public [minimum_score]} = CredentialVerification();
