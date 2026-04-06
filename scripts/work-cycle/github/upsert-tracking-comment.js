// Create or update the PR tracking comment.
//
// Finds an existing comment starting with "## PR Progress:" and updates it,
// or creates a new one if none exists.
//
// Expected environment:
//   PR_NUMBER, TRACKING_BODY

module.exports = async ({ github, context }) => {
  const prNumber = parseInt(process.env.PR_NUMBER);
  const body = process.env.TRACKING_BODY;

  const { data: comments } = await github.rest.issues.listComments({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: prNumber,
  });
  const existing = comments.find((c) => c.body?.startsWith("## PR Progress:"));

  if (existing) {
    await github.rest.issues.updateComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      comment_id: existing.id,
      body: body,
    });
  } else {
    await github.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      body: body,
    });
  }
};
