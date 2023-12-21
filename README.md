# Blackhawks Interview Presentation

## Description
The repo contains copies of all the relevant files for an advanced search feature that I developed as a part of a company website in order to allow
employees of the company to easily search for clients and their referrals. The framework used for this website is Django, but other technologies that
were utilized includes Bootstrap and Javascript. The full project was not copied to this repo for security reasons.

## Files Contained:
* `urls.py` (Contains all the Django paths for the project. Relevant lines: 70-73)
* `other_views.py` (Contains the views for the advanced search and results page. Relevant lines: 32-145)
* `models.py` (Contains the Client and Referral models that the search page uses. Relevant lines: 194-215, 488-507)
* `forms.py` (Contains the form used for the advanced search page. Relevant lines: 161-192)
* `search-advanced.html` (Template for the advanced search page.)
* `search-advanced-results.html` (Template for the advanced search results page.)
* `search.js` (Code to dynamically change the search fields based on what the user is searching for.)
