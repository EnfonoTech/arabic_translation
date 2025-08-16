app_name = "arabic_translation"
app_title = "Arabic Translation"
app_publisher = "Aravind R"
app_description = "English to Arabic Text Translation"
app_email = "aravindrajeshchry@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "arabic_translation",
# 		"logo": "/assets/arabic_translation/logo.png",
# 		"title": "Arabic Translation",
# 		"route": "/arabic_translation",
# 		"has_permission": "arabic_translation.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/arabic_translation/css/arabic_translation.css"
# app_include_js = "/assets/arabic_translation/js/arabic_translation.js"

# include js, css files in header of web template
# web_include_css = "/assets/arabic_translation/css/arabic_translation.css"
# web_include_js = "/assets/arabic_translation/js/arabic_translation.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "arabic_translation/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Item" : "public/js/item.js"
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "arabic_translation/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "arabic_translation.utils.jinja_methods",
# 	"filters": "arabic_translation.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "arabic_translation.install.before_install"
# after_install = "arabic_translation.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "arabic_translation.uninstall.before_uninstall"
# after_uninstall = "arabic_translation.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "arabic_translation.utils.before_app_install"
# after_app_install = "arabic_translation.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "arabic_translation.utils.before_app_uninstall"
# after_app_uninstall = "arabic_translation.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "arabic_translation.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"arabic_translation.tasks.all"
# 	],
# 	"daily": [
# 		"arabic_translation.tasks.daily"
# 	],
# 	"hourly": [
# 		"arabic_translation.tasks.hourly"
# 	],
# 	"weekly": [
# 		"arabic_translation.tasks.weekly"
# 	],
# 	"monthly": [
# 		"arabic_translation.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "arabic_translation.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "arabic_translation.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "arabic_translation.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["arabic_translation.utils.before_request"]
# after_request = ["arabic_translation.utils.after_request"]

# Job Events
# ----------
# before_job = ["arabic_translation.utils.before_job"]
# after_job = ["arabic_translation.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"arabic_translation.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

