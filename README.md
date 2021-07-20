# Ski Carinthia

## About

This is my fourth and final Milestone Project for the Full Stack Software Development Diploma with Code Institute. This project requires all elements of software development I have learned so far. It uses HTML, CSS and JavaScript for the front end and makes use of Python and the Django framework for the backend, which also uses the PostgreSQL relational database system.

This project is a website for skiers visiting Carinthia, Austria. It allows visitors to view ski areas/resorts/mountains, purchase tickets using the Stripe Authentication software as well as contribute to a form/blog on the website.

## UXD

### Strategy

I want any user to instantly recognise the purpose of the site, and to feel at ease every step of the way. There is no specific user base this website caters to, just the general public. To that end, the user stories below are non specific in terms of demographic, and only differentiate insofar as whether a user is a first time visitor, a general visitor, a logged in user or a shopper.

#### User Stories

User Story ID | As a user | I want to be able to | So that I can
--------------|-----------|----------------------|--------------
1|first time visitor|recognise the purpose of the site immediately|identify whether I am interested in the content and wish to use the site
2|general visitor|easily navigate the site on any device|easily use and navigate the site
3|general visitor|view a list of ski resorts|find which resort I would like to visit
4|general visitor|view individual ski resort details|identify which resort is best for my purposes
5|general visitor|view weather for ski resorts|identify which resort has the best conditions on a particular day
6|general visitor|easily register an account|make purchases/contribute to blog
7|logged in user|easily login/out|access my personal account
8|logged in user|reset password|access my personal account if I have forgotten my password
9|logged in user|have personal profile|view/update personal details and access ski pass
10|shopper|add items to shopping bag|prepare items for purchase 
11|shopper|see total of shopping bag|identify how much I will pay
12|shopper|modify shopping bag contents|make changes to bag if needed
13|shopper|checkout using credit/debit card|purchase ski passes
14|shopper|be notified if my card info is invalid and why|make necessary changes to card info
15|shopper|be notified if a purchase is successful|be sure that my purchase was successful
16|shopper|view order details|review my purchase
17|shopper|receive email confirmation of order|keep formal confirmation of my successful purchase
18|general visitor|view blogs|see blogs to get an idea of people's experiences
19|logged in user|add blog post|add personal post to website
20|general visitor|search for ski resort by name|find a particular resort
21|general visitor|use a map to see ski resort locations|find resort well located for me
22|general visitor|sort ski resorts|find resort suitable for me
23|admin/superuser|admin power to edit/delete blog posts entered by users|amend irrelevant or inappropriate content
24|admin/superuser|have crud power over all ski resorts|amend information if necessary

### Scope

The website is built as a minumum viable product. 

### Structure

The site has a simple layout, heavily influenced by the Bootstrap framework.

The navbar always sits at the top of each page, taking the user to all the site sections they can access. Only the pages relevant to the user are displayed e.g. a logged in user will not see a link to the 'login' page as they are logged in. Equally a logged out user will not see a link to the 'logout' page as they are alerady logged out. If a user tries to manually enter an invalid page url, they will be redirected automatically to the homepage. There is also a search bar on the navbar, prompting a user to search for a 'mountain' or resort.

The home page features call to action buttons for a user to immediately either view resorts or to view the blogs. There is also a button with a downward arrow at the bottom of the image which indicates to a user they can continue scrolling. The rest of the homepage contains links to filtered results of the resorts page. These are commonly desired ski resort 'types' such as family friendly resorts, or large, expansive resorts for example. The final section of the home page shows a map, displaying all of the resorts as tacks. Clicking on each tack opens up a tooltip with extra information to the resort and a link to the relevant detailed page.

Links and interactive elements are clearly signposted. Buttons have a colour scheme where 'positive' feedback buttons have green text, 'neutral' buttons have blue text and 'negative' buttons have red text. This is in line with the Bootstrap colour library (success, info and danger) but with the colours amended to suit the colour scheme for this project. 

### Skeleton

Below are the wireframes created in advance of starting the project. I used the wireframing software [Balsamiq](https://balsamiq.com/) for this project.

* Mobile Wireframe
  ![Wireframe for Mobile](documentation/wireframes/Mobile_Wireframe.png)

* Tablet Wireframe
  ![Wireframe for Tablet](documentation/wireframes/Tablet_Wireframe.png)

* Desktop Wireframe
  ![Wireframe for Desktop](documentation/wireframes/Desktop_Wireframe.png)

The wireframes were useful when constructing the site, but as can be seen on some pages, I deviated from the original design in some aspects. This was to be expected, as the wireframes only gave me a rough idea of what I wanted. For example, on the desktop version of the ski resort detail, the layout is significantly different in the final product. The wirefraem was still very useful when creating the page however, as it gave me a firm outline of all the most important features needed.

### Surface

I picked a very simple palette for this project. The standout scheme is a blue navbar, with an off-white main section below. This is to imitate a mountain scene with a blue sky and a white snow covered mountain below.

* #3F68B8 'True Blue' - used for navbar, card, input borders, 'neutral' buttons
* #F4F4F9 'Ghost White' - main background colour
* #343A40 'Gunmetal' - main text colour
* #008100 'Ao English' - used for 'positive' buttons
* #F95738 'Orange Soda' - used for 'negative' buttons

![Colour Pallette](documentation/ski-carinthia_palette.png)