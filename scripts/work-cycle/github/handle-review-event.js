// Handle a pull_request_review event on a work-cycle PR.
//
// On approval: post an advancing comment.
// On changes_requested: revert to contributor label and post feedback.

module.exports = async ({ github, context }) => {
  const prNumber = context.payload.pull_request.number;
  const reviewState = context.payload.review.state;
  const reviewBody = context.payload.review.body || "";
  const reviewer = context.payload.review.user.login;

  const { data: labels } = await github.rest.issues.listLabelsOnIssue({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: prNumber,
  });

  const stageLabel = labels.find((l) => l.name.startsWith("stage/"));
  if (!stageLabel) {
    console.log("No stage label found on PR, skipping");
    return;
  }

  const isWorkCyclePR = labels.some((l) => l.name.startsWith("work-cycle/"));
  if (!isWorkCyclePR) {
    console.log("Not a work cycle PR, skipping");
    return;
  }

  if (!stageLabel.name.startsWith("stage/review-")) {
    console.log(
      `Current stage ${stageLabel.name} is not a review stage, skipping`
    );
    return;
  }

  if (reviewState === "approved") {
    await github.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      body: `✅ **${reviewer}** approved at stage \`${stageLabel.name}\`. Stage advancing.`,
    });
  } else if (reviewState === "changes_requested") {
    const contributorLabel = "stage/developer";

    try {
      await github.rest.issues.removeLabel({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: prNumber,
        name: stageLabel.name,
      });
    } catch (e) {
      console.log(`Could not remove label: ${e.message}`);
    }

    try {
      await github.rest.issues.getLabel({
        owner: context.repo.owner,
        repo: context.repo.repo,
        name: contributorLabel,
      });
    } catch {
      await github.rest.issues.createLabel({
        owner: context.repo.owner,
        repo: context.repo.repo,
        name: contributorLabel,
        color: "0e8a16",
        description: "Work cycle stage: contribute",
      });
    }

    await github.rest.issues.addLabels({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      labels: [contributorLabel],
    });

    await github.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      body: [
        `🔄 **${reviewer}** requested changes at stage \`${stageLabel.name}\`.`,
        `Stage reverted to \`${contributorLabel}\`.`,
        "",
        "**Review feedback:**",
        `> ${reviewBody.replace(/\n/g, "\n> ")}`,
        "",
        "The contributor agent will be invoked to address this feedback.",
      ].join("\n"),
    });
  }
};
