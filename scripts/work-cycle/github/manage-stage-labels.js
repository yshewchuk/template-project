// Manage stage labels on a work-cycle PR.
//
// Removes all existing stage/* labels, then applies the new one.
// Creates the label if it doesn't exist yet.
//
// Expected environment/input:
//   PR_NUMBER, STAGE_LABEL, STAGE_TYPE

module.exports = async ({ github, context }) => {
  const prNumber = parseInt(process.env.PR_NUMBER);
  const stageLabel = process.env.STAGE_LABEL;
  const stageType = process.env.STAGE_TYPE;
  const labelColor = stageType === "contribute" ? "0e8a16" : "1d76db";

  const { data: labels } = await github.rest.issues.listLabelsOnIssue({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: prNumber,
  });

  for (const label of labels) {
    if (label.name.startsWith("stage/")) {
      try {
        await github.rest.issues.removeLabel({
          owner: context.repo.owner,
          repo: context.repo.repo,
          issue_number: prNumber,
          name: label.name,
        });
      } catch (e) {
        console.log(`Could not remove label ${label.name}: ${e.message}`);
      }
    }
  }

  try {
    await github.rest.issues.getLabel({
      owner: context.repo.owner,
      repo: context.repo.repo,
      name: stageLabel,
    });
  } catch {
    await github.rest.issues.createLabel({
      owner: context.repo.owner,
      repo: context.repo.repo,
      name: stageLabel,
      color: labelColor,
      description: `Work cycle stage: ${stageType}`,
    });
  }

  await github.rest.issues.addLabels({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: prNumber,
    labels: [stageLabel],
  });
};
