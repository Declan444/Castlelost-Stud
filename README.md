# Grange Equestrian

## The equestrian centre to book a horse riding lesson

Grange Equestrian was developed to allow beginners, intermediate and advanced riders to be able to book a riding lesson with an instructor of choice. The user can enter the site or app, read about the different types of lessons, read about the instructors and then book a lesson that is available. The site is intended to give the user all the information that they would need to enable them to make an informed choice of which lesson and which instructor they need to book. The booking process shows days available and timeslots within those days for the user to book. Once booked the user is shown exactly what they have booked which awaits approval by the instructor. 

The site also allows the user to view all comments made by other users who have had a that specific lesson. If the user has had a lesson they can then leave a comment on that specific lesson. The users can also delete a comment or edit a comment that they have left on the lesson.

### Project Overview

The Grange Equestrian site is intended to offer a user-friendly interface to allow the users to browse, review, learn and book a riding lesson.The project is designed to show the use of the latest web technologies and follows best practices in web development. The project follows the core structure of the Code Institute Blog walkthrough with the use of django and deploying to heroku and the setting up of the project. The project implements a date, timeslot and booking system to enable users to book a lesson. It also gives the user front end crud capability by allowing them to create, read, update and delete comments.

[Live Demo](https://castlelost-stud-cbac18c58c5b.herokuapp.com/)

### Key Features

- Booking capability
- Responsive design for various devices
- Ability to leave comments on lesson
- CRUD capability for user
- CRUD capability for Admin
- Ability for admin to add lessons and instructors through backend
- User authentication and profile management

### Target Audience

The site is designed for anybody interested in horse riding. This includes beginners, intermediate and advanced riders. 

## Table of Contents

1. [Features](#features)
    - [Key Features Summary](#key-features-summary)

2. [User Experience (UX)](#user-experience-ux)
    - [User Stories](#user-stories)
    - [Design Choices](#design-choices)
    - [Wireframes](#wireframes)

3. [Information Architecture](#information-architecture)
    - [Flowchart](#flowchart)
    - [Database Schema (ERD Diagram)](#erd-diagram)
    - [Data Models Description](#data-models-description)

4. [Technologies Used](#technologies-used)
    - [Languages](#languages)
    - [Frameworks](#frameworks)
    - [Databases](#databases)

5. [Agile Methodology](#agile-methodology)

6. [Deployment](#deployment)

7. [Testing](#testing)

8. [Bugs and Fixes](#bugs-and-fixes)

9. [Unsolved Issues and Bugs](#unsolved-issues-and-bugs)

10. [Credits](#credits)

## Features

### Key Features Summary

    - Home page with book a lesson button
    - User registration and login with form validation and error handling
    - Django admin panel for superuser to manage, users, bookings, instructors and lessons
    - Customised 404 error pages
    - Booking capability for date and time slots
    - Ability to comment on a lesson
    - Full front end CRUD capability
    - Ability to view lesson comments
    - Lesson types dynamically served from the backend
    - Detailed explanation for each lesson type
    - Contact us capability for the user
    - select an instructor

## User Experience (UX)

### Project Goals

#### Site Owner Goals

The site owner goals was to allow a user to visit the site, easily be able to navigate around the site, to be able to easily and logically review lessons available, get details about the lessons and then to be able to book a lesson with a date and an available timeslot. The site owner goals was also for the use to understand that they had to be registered to enable them to book a lesson and to do this they had to be able to register easily. Once registered the user would easily be able to login to the site and from there logically and easily book a lesson. The site owner also wanted the User to know which lesson, the date and timeslot that they had just booked. 

#### User Goals

The user goals were to be able to easily book a lesson. The user wants to easily know how to book a lesson, and to have the ability to select and avalable date and within that date to be able to select an available timeslot. The user wants to be able to easily know if a timeslot is not available and not have the ability to book this date or timeslot. The user wants to also be told what they have actually booked. The user wants to be able to navigate logically and easily around the site and always have the ability to return to the home page. The user can also select an instructor.

### User Stories
User stories were used to drive this project. 
[User Stories (github issues)](https://github.com/Declan444/Castlelost-Stud/issues)
<br>
Kanban Board was used to control the project flow.
[Kanban Board (github project)](https://github.com/users/Declan444/projects/11)

All user stories acceptance criteria were met in this project. All issues were completed.

### Design Choices
#### Colour Scheme
The colour scheme is 
![Shades of #445261](image.png)

#### Typography
For this project I choose Roboto as is modern and suited my concept.

#### Imagery
All imagery is the property of Grange Equestrian and shows, horses and showjumping which depicts the theme of the site.


### Wireframes

Home Page

![Home Wireframe](castleloststud\readme_assets\images\wireframes\grange_home.png)



