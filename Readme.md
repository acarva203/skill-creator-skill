## Introduction

Claude skills act like a structured guide for the model. 

Find yourself prompting Claude to do the same task one too many times? Need a task to be done with an automatic trigger? 
**You should consider creating a Claude Skill.
**

Within claude.ai itself, there are built-in skills that Anthropic has built for convenience such as docx to create and process documents, pptx to create and process slide decks, and most well known, skill-creator to create new skills. 

Anthropic's skill-creator has the model outline the skill structure, test with sample prompts, evaluate results qualitatively and quantitatively, and iterate until the user is satisfied with the newly created skill. It's intentionally structured for both technical and non-technical folks, so it chooses to explain the skill structure e.g. frontmatter, YAML, progressive disclosure, etc. selectively. 

## Skill Description
This repo contains my version of a skill-creator skill (to avoid confusion, all references to a skill creator skill from this point will refer to the one that I made). 

Similar to Anthropic's version, my frontmatter's description starts with the purpose to build new skills, but goes one step forward and includes key trigger phrases like "create a skill". This is inspired by my work this week building a internal branding presentation tool where automatically triggering said skill proved convenient. 

This skill has multiple reference files to account for different aspects of skill creation. One file exists to optimize the description which is one of the first things Claude will read while loading up the skill. Another holds the structure of the skill including frontmatter, steps, and more. The workflow file is a more detailed look into how to build a skill from asking key questions to scaffolding the directory to testing andc evaluating.

To ensure that the skill performs optimally, we have two types of verification in the evals file as well as the grilling file. The evals file reviews the outputs of the new skill quantatitatively and qualitatively similar to Anthropic's version. The grilling file establishes an iterative loop to resolve uncertainties and edge cases.

In the scripts folder, these premade scripts allow Claude to quickly scaffold the file directory for the new skill as well as package the skill once the building is done.

To add this skill to your Claude environment, download this file as a zip file and upload to Claude by clicking Skills > Manage Skills > + > Upload > then upload the zip file.

Beyond Claude, you can also use these skills with other AI platforms such as Codex. While this specific skill has been optimized for Claude, I would be curious to see how it performs on other models. 

