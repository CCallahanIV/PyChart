# [PyChart](https://github.com/CCallahanIV/PyChart)
Code Fellows 401 Python Final Project

## Members:
 * Ted Callahan
 * Jordan Schatzman
 * Colin Lamont

PyChart is web-based application allowing the user a simple sandbox environment in which to upload or access data through API and render and save representations of that data.

## User Stories:

 * As a User...
   - I want to be able to upload a .csv, perform very simple data manipulation, and render it into a chart.
   - I want to be able to visualize either my data or preexisting data in the form of a scatterplot, histogram or bargraph.
   - I want to store my data and renders on my profile.
   - I want to be able to download my saved renders.
   - I want some simple customization options on my renders.
 * As a Developer...
   - I want to use a common python library (e.g. bokeh) to manipulate data and render it in a web application.
   - I want to be have 5 tests written per developer per day.
   - I want to host this application on AWS.
   - I want to be able to automate deployments with ansible.
   - I want to share responsibilities with other devs so we all learn.
   - I want the app to be built using django.

## Git Workflow:
 
 * Git Master - One person in the group will control Pull Requests from development to master and control the deployment pipeline.

 * Issue Tracking - Feature Production and issues will be tracked using Waffle. [https://waffle.io/CCallahanIV/PyChart]

 * Deployment Branch: master 
   - All pull requests to master may only be approved by the Git Master.
   
 * Staging Branch: development
   - All work will be merged into the development branch via pull request.  
   - Developers may not merge their own PR, all PR's must be reviewed by another dev.
   
 * Feature Branches: by feature name
   - All features should have descriptive names.
   
 * Hotfix-Branches: <feature or development>-hotfix
   - Hotfix branches may be made off of any feature branch or the development branch to quickly fix small issues.
