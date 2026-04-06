// Post a comment requesting human (Product Manager) review.
//
// Expected environment:
//   PR_NUMBER, WORK_CYCLE

module.exports = async ({ github, context }) => {
  const prNumber = parseInt(process.env.PR_NUMBER);
  if (!prNumber) {
    console.log("No PR number provided, skipping human review request");
    return;
  }

  const workCycle = process.env.WORK_CYCLE;

  await github.rest.issues.createComment({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: prNumber,
    body: [
      "## Human Review Requested",
      "",
      `All automated stages for the **${workCycle}** work cycle are complete.`,
      "This PR is ready for **Product Manager** review.",
      "",
      "Please review the changes and:",
      "- **Approve** the PR if the changes satisfy requirements",
      "- **Request changes** with feedback if adjustments are needed",
    ].join("\n"),
  });
};
