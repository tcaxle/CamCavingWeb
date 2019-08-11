# CamCavingWeb
Cambridge University Caving Club (CUCC) website repository

## To Do
- [x] Basic Sitemap
- [x] Static pages app "StaticPages"
- [x] "base.html" page template
- [x] Migration of basic static pages from old wiki
- [ ] Extract all documents, images, misc files from old wiki and restructure archive
- [ ] Layout database: list of tables, fields, mappings
- [ ] Authentication and Accounts App (one-to-one user model for extra details)
- [ ] Gear Hire App "Gear"
- [ ] Blog app "Blog"
- [ ] ? Treasury app "BankOfCaving"

# Site Layout
## Apps
### StaticPages
This app holds the static pages of the app. Mainly, this means the "public" half of the site: the homepage, about pages and suchlike.

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
