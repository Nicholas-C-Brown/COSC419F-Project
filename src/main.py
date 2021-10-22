from linkedin_helper import linkedin_profile_baseurl as profile_baseurl, linkedin_exampleurl as example_url, login, validate_profile_url
from driver_helper import configure_driver as configure, scroll_down, scroll_until_find_by_class_name




driver_path = 'COSC419F-Project/assets/driver/chromedriver.exe'
is_headless = False

# APPLICATION START

# Get url from user
print("Enter your LinkedIn profile URL.")
url = profile_baseurl + input(profile_baseurl)

if(not validate_profile_url(url)):
    print("\nPlease enter a valid url.\nExample: " + example_url)
    exit


# Start Chrome Webdriver and Login
driver = configure(driver_path, is_headless)
login(driver)

# Go to user's profile page
driver.get(url)

# Get user's information
name_element = driver.find_element_by_class_name('text-heading-xlarge.inline.t-24.v-align-middle.break-words')

profile_element = driver.find_element_by_class_name('profile-detail')
bio_element = profile_element.find_element_by_class_name('inline-show-more-text.inline-show-more-text--is-collapsed.mt4.t-14')

skills_element = scroll_until_find_by_class_name(class_name='pv-profile-section.pv-skill-categories-section.artdeco-card.mt4.p5.ember-view', driver=driver, parent=profile_element)
skills_show_more_button = scroll_until_find_by_class_name(class_name='pv-profile-section__card-action-bar.pv-skills-section__additional-skills.artdeco-container-card-action-bar.artdeco-button.artdeco-button--tertiary.artdeco-button--3.artdeco-button--fluid.artdeco-button--muted', driver=driver, parent=skills_element)
skills_show_more_button.click()

# Top 3 Skills listed
skills_top_list_element = skills_element.find_element_by_class_name('pv-skill-categories-section__top-skills.pv-profile-section__section-info.section-info.pb1')
skills_top_list_li_elements = skills_top_list_element.find_elements_by_css_selector('li')
# The rest of the skills
skills_extra_list_element = skills_element.find_element_by_id('skill-categories-expanded')
skills_extra_list_li_elements = skills_extra_list_element.find_elements_by_css_selector('li')

# Agglomerate all skill li elements
skills_li_elements = []
[skills_li_elements.append(s) for s in skills_top_list_li_elements]
[skills_li_elements.append(s) for s in skills_extra_list_li_elements]

# Store all skill text elements in a list
skills_elements = []
[skills_elements.append(s.find_element_by_class_name('pv-skill-category-entity__name-text.t-16.t-black.t-bold')) for s in skills_li_elements]

print("")
print("Name: " + name_element.text)
print("About: " + bio_element.text)
print("Skills: " )
[print("    -" + s.text) for s in skills_elements]
print("")

