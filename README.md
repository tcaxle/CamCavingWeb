# CamCavingWeb
Cambridge University Caving Club (CUCC) website repository

## To Do
- [x] Basic Sitemap
- [x] Static pages app "StaticPages"
- [x] "base.html" page template
- [x] Migration of basic static pages from old wiki
- [x] Extract all documents, images, misc files from old wiki and restructure archive
- [x] Migrate all pages or archive them into the legacy folders
- [x] Provide links on relevant pages to relevant documents and archive/legacy
- [x] Migrate master to Caving SRCF socuser. All further changes to be done on sepeate dev branches.
- [x] Layout database: list of tables, fields, mappings
- [x] Organise SSL and new domain
- [x] Authentication and Accounts App (one-to-one user model for extra details)
- [x] Gear tape page to be Guinea Pig
- [x] Gear Hire App "Gear"
- [x] Blog app "Blog"
- [x] ? Treasury app "BankOfCaving"

# Site Layout
In the root of the site ("CamCavingWeb") is the urls.py and views.py for all the static pages on the site.

## Apps
### Blog
This app holds the pages with the blog functionality. The blog is used for all user posts of any kind. Different kinds of post (trip logs, announcements, articles etc.) are handled by tags. Relevant pages are then set up to display different tagged posts.

- /Meets/Blog/ shows trip all posts, it is the "master" blog page. It has options to filter by tags as desired. By default, it filters by the "trip" tag.
- /Meets/Social/ shows all posts with the "social" tag.
- /Meets/Training/ shows all posts with the "training" tag.

### Gear
This app manages all of the club's gear inventories, logging, and hiring systems. It allows users to:

- Sign gear in/out of the tackle store. Different types of gear are differentiated between "personal" hire and "trip" use.
- Access the gear inventory to add/edit/retire items of gear.

### BankOfCaving
This app may or may not exist. If I get around to it, it will handle all club finances. It will integrate gear hire, meet and membersip fees, and bank account balance.
