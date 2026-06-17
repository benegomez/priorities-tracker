MVP Definition

Purpose

The purpose of the Minimum Viable Product (MVP) is to validate the core value proposition of Priorities Tracker:

Provide managers with clear visibility into weekly commitments, execution results, and commitment reliability without introducing unnecessary complexity or administrative burden.

The MVP focuses on a lightweight weekly planning and accountability process that helps managers answer three fundamental questions:

1. What did each team member commit to?
2. What did they accomplish?
3. How reliably do they deliver on their commitments?

The MVP intentionally avoids becoming a project management platform and instead focuses on commitment management and execution visibility.

⸻

Product Scope

The MVP is designed around a weekly planning cycle composed of:

1. Planning commitments.
2. Tracking progress.
3. Recording outcomes.
4. Measuring reliability.

The product serves three primary user groups:

* Administrators
* Employees
* Managers

⸻

Administration Capabilities

The administration module provides the organizational structure required to support planning and reporting.

User Management

Administrators can manage platform users.

Features

* Create users
* Edit users
* Activate users
* Deactivate users
* Assign roles
* Assign teams
* Assign managers

Supported Roles

* Administrator
* Manager
* Employee

⸻

Team Management

Administrators can manage team structures.

Features

* Create teams
* Edit teams
* Assign employees
* Assign managers
* Visualize team structure

⸻

Project Management

Projects exist solely for categorization and reporting purposes.

The platform does not attempt to manage schedules, dependencies, sprint boards, or project execution workflows.

⸻

Projects

Features

* Create project
* Edit project
* Activate project
* Deactivate project
* Assign participants

Data Model

* Name
* Description
* Status
* Owner

⸻

Project Phases

Project phases provide additional categorization for priorities.

Example

Project:

CRM Implementation

Phases:

Discovery
Design
Development
Testing
Deployment

Features

* Create phase
* Edit phase
* Associate priorities with phases

⸻

Employee Experience

The employee experience is built around two primary workflows:

* Weekly Check-In
* Weekly Check-Out

⸻

Weekly Check-In

Objective

Capture commitments for the upcoming week.

The Check-In is the primary activity performed by employees.

The process should be completable in less than five minutes.

⸻

Workflow

1. Select project
2. Select phase
3. Create priorities
4. Create tasks
5. Reuse pending priorities
6. Register anticipated risks
7. Submit Check-In

⸻

Priority Management

Priorities represent the commitments an employee intends to complete during the week.

Features

* Create priority
* Edit priority
* Duplicate priority
* Reuse previous priorities
* Associate project
* Associate phase

Data Captured

* Name
* Description
* Project
* Phase
* Priority level
* Status

⸻

Task Management

Tasks represent work items associated with priorities.

Features

* Create task
* Edit task
* Mark complete
* Carry forward

Data Captured

* Name
* Description
* Status

⸻

Weekly Progress Tracking

Employees may update progress during the week without waiting for the Check-Out process.

⸻

Progress Updates

Features

* Update status
* Add comments
* Add notes

⸻

Blocker Management

Features

* Create blocker
* Update blocker
* Resolve blocker

Suggested Categories

* External dependency
* Missing information
* Technical issue
* Changing priorities
* Pending approval

⸻

Risk Management

Features

* Create risk
* Update risk
* Mark mitigated

⸻

Weekly Check-Out

Objective

Capture execution results and completed commitments.

The Check-Out represents the second most important workflow within the platform.

⸻

Workflow

1. Review priorities
2. Mark completed tasks
3. Mark completed priorities
4. Add comments
5. Record lessons learned
6. Review blockers
7. Identify continuing work
8. Submit Check-Out

⸻

Automatic Continuity

One of the most important usability features of the MVP.

Features

* Carry forward unfinished priorities
* Carry forward unfinished tasks
* Generate draft for next week’s Check-In

Benefits

* Reduced administrative effort
* Improved continuity
* Better user adoption

⸻

Manager Experience

Managers consume information rather than create it.

Their primary objective is obtaining visibility into team commitments and execution.

⸻

Team Dashboard

Provides an aggregated view of team activity.

Displayed Information

* Employee
* Active priorities
* Completed priorities
* Blockers
* CRS

⸻

Weekly View

Answers:

* Who completed Check-In?
* Who completed Check-Out?
* What priorities exist?
* What is at risk?

⸻

Individual View

Allows managers to review a single employee.

Includes:

* Priorities
* Tasks
* Risks
* Blockers
* CRS
* Historical performance

⸻

Commitment Reliability Score (CRS)

The flagship capability of the MVP.

Objective

Measure commitment reliability over time.

Inputs

* Committed priorities
* Completed priorities
* Committed tasks
* Completed tasks
* Carried-over priorities
* Historical consistency

⸻

Reporting

The MVP includes basic reporting capabilities.

⸻

Individual Report

Displays:

* Priority history
* Completion history
* CRS evolution

⸻

Team Report

Displays:

* Average completion
* Weekly trends
* Open risks
* Recurring blockers

⸻

Project Report

Displays:

* Active priorities
* Completed priorities
* Risks
* Completion trends

⸻

Artificial Intelligence

The MVP includes a limited AI capability focused on summarization.

⸻

Weekly Summary

Automatically generates executive summaries.

Example:

This week the team completed 87% of committed work. Three priorities are at risk and two recurring blockers were identified.

⸻

Out of Scope

The following capabilities are intentionally excluded from the MVP:

* Project scheduling
* Gantt charts
* Scrum boards
* Kanban boards
* Time tracking
* Resource planning
* Portfolio management
* Complex workflow automation
* Enterprise integrations
* Organizational benchmarking

⸻

Success Criteria

The MVP is successful if managers can consistently answer:

1. What did each employee commit to?
2. What did they complete?
3. How reliable are they at delivering commitments?

without requiring constant meetings, status requests, or manual reporting.

⸻

MVP Summary

The MVP consists of:

Administration

* Users
* Teams
* Projects
* Phases

Employees

* Check-In
* Check-Out
* Priorities
* Tasks
* Automatic Continuity

Managers

* Team Dashboard
* Weekly View
* Individual View

Metrics

* Weekly Completion
* CRS

AI

* Weekly Summary

This scope preserves the product’s central objective:

Improve execution visibility and commitment reliability through simple, measurable weekly commitments.