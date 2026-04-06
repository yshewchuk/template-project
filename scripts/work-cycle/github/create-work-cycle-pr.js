// Create a work-cycle PR with the appropriate label.
//
// Expected environment:
//   PR_TITLE, PR_BODY, HEAD_BRANCH, WORK_CYCLE_LABEL

module.exports = async ({ github, context, core }) => {
  const { data: pr } = await github.rest.pulls.create({
    owner: context.repo.owner,
    repo: context.repo.repo,
    title: process.env.PR_TITLE,
    body: process.env.PR_BODY,
    head: process.env.HEAD_BRANCH,
    base: "main",
    draft: false,
  });

  await github.rest.issues.addLabels({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: pr.number,
    labels: [process.env.WORK_CYCLE_LABEL],
  });

  core.setOutput("number", pr.number);
};
