## 19/12/22 Changelog
- Done homepage basic layout
- Done create user layout (Layout subject to change)
- Done edit user layout (Layout subject to change)
- Change formHelper html to suit needs
- Replace form fields to use formHelper macro function
- Form fields now shows a red star if the field is required, hovering it will show a tooltip
- Added icons to user options dropdown
- Added footer
- Added app icons in 1024 and 512 px resolutions
- Removed some redundant CSS classes

## 20/12/22 Changelog
- Change user class admin variable to accountType to handle 3 different user types (Customer, doctor and delivery)
- formHelper now supports wtforms RadioField

## 21/12/22 Changelog
- Done admin change password page and functionality
- Done zoom functionality
- Created delivery address class
- Removed delivery info fields from edit/create user pages

## 22/12/22 Changelog
- Added accessibility (zoom) options for guests

## 23/12/22 Changelog
- Added Address list and add address pages
- Done functionality for adding addresses and listing all addresses
- Minor text changes
- Zoom feature is somewhat available on firefox using transform scale (still broken)

## 25/12/22 Changelog
- Added edit address page
- Moved delivery address storage into User class instead of storing it as a standalone class
- Added delete user page
- Minor UI improvements

## 26/12/22 Changelog
- Re-factored all adminUser routes to handle non-existent email accounts
- Added edit user functionality
- Birthday and phone numbers now stores in DB when adding or editing users

## 27/12/22 Changelog
- Moved some form validations to forms.py and use ValidationError to show errors instead
- FormHelper now supports submit buttons

## 28/12/22 Changelog
- Improved navbar layout
- Added new items into the admin navbar (Treatments, Orders, Blog, About)
- Created new classes (products, treatments, coupons)
- Created directories for respective pages and moved templates into it
- Created delivery partner navbar layout in adminNavControls.html
- Created view all treatments page
- Minor UI changes