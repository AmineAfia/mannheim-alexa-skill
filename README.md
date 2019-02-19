# Mannheim Skill

This repo includes the code for the Mannheimer Morgen skill. The structure of the repo is the standard structure of alexa skills generated by ask CLI, in addition the folder Soumya_ML includes the code for the prediction model:

```
.ask            Config for ask CLI
hooks           Hooks used for deployment
instructions    The tutorial we followed at the bigining to learn about alexa developement
lambda          that's the backend of our skill (What we deploy to the lambda function)
models          Our VUI definition
Soumya_ML       Prediciton model
skill.json      Infos that get shown about the app amazon store + apis definition (in this case lamda definition)
```

# ask CLI

The skeleton of the skill was generated and deployed using ask CLI. [link](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html)
