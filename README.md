# [PyChart](https://github.com/CCallahanIV/PyChart)
Code Fellows 401 Python Final Project

## Members:
 * Ted Callahan
 * Jordan Schatzman
 * Colin Lamont

PyChart is web-based application allowing the user a simple sandbox environment in which to upload or access data through API and render and save representations of that data.

## User Stories:
(Relative difficulty rankings are included at the end of each story, or as a part of the story in parenthesis.)
User and Dev stories are ranked in order.

The MVP, INTERMEDIATE, and STRETCH tags below define milestones for our application.  Each place represents a potential stopping point were we could present a proof-of-concept.  Our MVP goal is to have an application where a user can upload a .csv file, examine the data, and render an chart image.  The data and render can saved to a profile.

To add to that, we would like to offer the user some options to customize the render and data.  As time allows, we would like to add more options for customization of data and renders.


 * As a User...
   1. I want to be able to upload a .csv (2), perform very simple data manipulation (6), and render it into a chart (4). 
   2. I want to store my data and renders on my profile. (3)
-- MVP --
   3. I want some simple customization options on my renders (5).
-- INTERMEDIATE --
   4. I want to be able to visualize either my data or preexisting data in the form of a scatterplot, histogram or bargraph. (4)
   5. I want to be able to download my saved renders. (1)
-- STRETCH -- 

 * As a Developer...
   0. I want to share responsibilities with other devs so we all learn. (1)
   1. I want the app to be built using django. (2)
   2. I want to use a common python library (e.g. bokeh) to manipulate data and render it in a web application. (6)
   3. I want to be have 5 tests written per developer per day. (3)
   4. I want to host this application on AWS. (5)
   5. I want to be able to automate deployments with ansible. (7)

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
