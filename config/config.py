from selenium.webdriver.common.by import By
#BROWSER
BROWSER = "chrome"
#VERSION################################
VERSION = 'Version: 2.3.1'
GEOLOGY_VERSION = 'Geology (Version:1.0.23_2)'
#ENVIRONMENT
TEST_ENVIRONMENT = 'QA Server'
TESTED_BY = 'QA AUTOMATION TEAM'
#URL####
BASE_URL = "https://qa.broadbandiq.com/"
#USERS######################################################################
# USERNAME = "nikitha.deshpande@vcti.io"
# PASSWORD = "ApS@1234"
USERNAME = "santhosh.s@vcti.io"
PASSWORD = "Santhosh@31"
############################################################################
# USERNAME = "vidhyashree.n@vcti.io"
# PASSWORD = "Vidhya@123"
############################################################################
#DRIVER#
EDGE_DRIVER_PATH = "./browserDriver/msedgedriver.exe"
CHROME_DRIVER_PATH = "./browserDriver/chromedriver.exe"
############################################################################
#COUNTY_NAMES
COUNTY_NAME = 'Maricopa County, AZ'
COUNTY_NAME1 = 'Smith County, TX'        #middle mile lens
COUNTY_NAME2 = 'Kitsap County, WA'  #tax boundaries lens
COUNTY_NAME3 = 'Santa Clara County, CA' #Etheric Networks lens
COUNTY_NAME4 = 'Jefferson County, PA' #First Light Fiber lens
COUNTY_NAME5 = 'Wichita County, TX' #Dobson Fiber
COUNTY_NAME6 ="Union County, OR"#Location Lens
COUNTY_NAME7 = "Kings County, NY"
COUNTY_NAME8 = "Douglas County, NE"  #client lens : COX and ISP fiber
COUNTY_NAME9 = "Cleveland County, OK" #client lens : COX and ISP fiber
COUNTY_NAME10 = "Queens County, NY"  #client lens : skywire
COUNTY_NAME11 = "Gregg County, TX" #client lens : Cable One
COUNTY_NAME12 = "Clarke County, GA"     #Location lens
COUNTY_NAME13 = "Ada County, ID"
COUNTY_NAME14 = "Autauga County, AL"
COUNTY_NAME15 = "Lincoln County, CO"
COUNTY_NAME16 = "Campbell County, KY"
COUNTY_NAME17 = "Orange County, FL"
COUNTY_NAME18 = "Vieques Municipio, PR"
COUNTY_NAME19="Webster Parish, LA"
COUNTY_NAME20= "Lee County, AL"
COUNTY_NAME21 = "Orange County, FL"
COUNTY_NAME22 = 'Montgomery County, TX'
COUNTY_NAME23 = "Dallas County, TX"
COUNTY_NAME24 = "Baldwin County, AL"
#########################################################################

PROVIDER = 'Altice USA (Optimum)'   #ISP FOOTPRINT
TECHNOLOGY = "All" #ISP FOOTPRINT SELECTING TECHNOLOGY
TECHNOLOGY1 = "Fiber to the Premises" #ISP Footprint Selecting different technology
#ISP FOOTPRINT SELECTING CATEGORY###########
CATEGORY = "Residential"
CATEGORY1 = "Business"
CATEGORY2 = "Both"
#################################################

#user details
USER_SEARCH_NAME = "vidhya"
USER_EMAIL = "vidhyashree.n@vcti.io"
USER_FIRST_NAME = "Vidhyashree"
USER_LAST_NAME = "Nedumaran"
USER_PACKAGE = "Master Package"
##################################################################################

LENS1 = 'fiber-growth'
LENS2 = 'middle-mile'
LENS3 = 'road-density'
TOOL1 = "Display ISP Footprint"
TOOL2 = 'Report Bug'
SERVICE_PROVIDER_NAME1 = 'AT&T'
AGE_SEARCH = '10-14'
NAME = "Santhosh S"
ZIP_CODE = "10021"
City_Town_CDP = "Splendora city, TX"
STATE = "Texas"
CO_ORDINATES = "30.1556, -95.1604"
MUNCIPAL_AREA = "Smith River-Gasquet CCD - Del Norte County, CA"
MUNCIPAL_AREA2 = "Arriba CCD - Lincoln County, CO"
targets = ["Municipal Areas", "City/Town/CDP"]
FIBER_DATA = r"C:\Users\Velankani\Downloads\ftth_insights_comparision.xlsx"
POINT_COUNTY_CO_ORDINATES = "30.47482721,-87.86689173"


############################################################################################

##########################################################################################
#logs
PAGES_NUMBER = "2"
LOGS_ACTIVITY = "search"
LOGS_REGION = "Maricopa County, AZ"
LOGS_REGION_TYPE = "County"
LOGS_ADDRESS = 'TEXAS'
LOGS_STATUS = 'success'
LOGS_STATUS_FAILURE = 'failure'
ACTIVITY_AREA = 'Splendora'
ACTIVITY_ACTIVITY = "Search"
ACTIVITY_SERVICE_PROVIDER = "Optimum"
CO_ORDINATES = "30.1556, -95.1604"
PAGES_NUMBER = "2"
RITTER_COUNTY_CO_ORDINATES = "32.61443246027341, -93.28930924417891"

########
COUNTIES_LIST = ['Smith County, TX','Maricopa County, AZ',"Kitsap County, WA","Kings County, NY","Douglas County, NE","Queens County, NY"]
SEARCH_COUNTY_TOAST_MESSAGE = "Loading too many Census Blocks may impact browser performance and user experience."
HOA_MONTGOMERY_COUNTY_CO_ORDINATES = "30.462225397609544, -95.54477433289418"
CABLE_ONE_CO_ORDINATES = "32.526845879051656, -94.76361427116427"
timeout_value = 60
poll_frequency_value = 1
SALES_TERRITORY_DESCRIPTION = "Added to Sales Territory by Automation"
NETWORK_DISTRIBUTION_VALUE = "Automated message"
PROXIMITY_VALUE = "4000"
CONTEXT_MENU_GOOGLE_VIEW_VALUE = 'Google View'
CONTEXT_MENU_BING_VIEW_VALUE = 'Bing View'
CONTEXT_MENU_FCC_VALUE = 'FCC View'
GOOGLE_VIEW_TITLE =  '28°33\'03.1"N 81°19\'03.8"W - Google Maps'
SALES_TERRITORY_NAME = "Nikitha Deshpande"
SALES_TERRITORY_SPECIFIC_USER = 'hotwire user'

########################################
MIDDLE_MILE_COUNTY = {
    "Accelecom" :"Alabama",
    "Conterra Networks":"Arizona",
    "Cox Communications":"Oklahoma",
    "Dobson Fiber":"Arkansas",
    "Etheric Networks":"California",
    "Ezee Fiber":"New Mexico",
    "FirstLight Fiber":"Florida",
    "Windstream":"Delaware"
}



MIDDLE_MILE_PROVIDER1 = "Accelecom"
MIDDLE_MILE_PROVIDER2 = "Conterra Networks"
MIDDLE_MILE_PROVIDER3 = "Cox Communications"
MIDDLE_MILE_PROVIDER4 = "Dobson Fiber"
MIDDLE_MILE_PROVIDER5 = "Etheric Networks"
MIDDLE_MILE_PROVIDER6 = "Ezee Fiber"
MIDDLE_MILE_PROVIDER7 = "FirstLight Fiber"
MIDDLE_MILE_PROVIDER8 = "Windstream"
MIDDLE_MILE_PROVIDER9 = "Bluebird Fiber Network"
MIDDLE_MILE_PROVIDER10 = "Dublink Fiber"
MIDDLE_MILE_PROVIDER11 = "Fiber Light"
MIDDLE_MILE_PROVIDER12 = "Harbor Link Fiber"
MIDDLE_MILE_PROVIDER13 = "Metro Marine Fiber Networks"
MIDDLE_MILE_PROVIDER14 = "Renville County Hub"
MIDDLE_MILE_PROVIDER15 = "South Front Networks"
MIDDLE_MILE_PROVIDER16 = "Viaero Fiber"



MIDDLE_MILE_STATE_VALUE1 = "Alabama"
MIDDLE_MILE_STATE_VALUE2 = "Arizona"
MIDDLE_MILE_STATE_VALUE3 = "Oklahoma"
MIDDLE_MILE_STATE_VALUE4 = "Arkansas"
MIDDLE_MILE_STATE_VALUE5 = "California"
MIDDLE_MILE_STATE_VALUE6 = "New Mexico"
MIDDLE_MILE_STATE_VALUE7 = "New Hampshire"
MIDDLE_MILE_STATE_VALUE8 = "Delaware"
MIDDLE_MILE_STATE_VALUE9 = "Missouri"
MIDDLE_MILE_STATE_VALUE10 = "Ohio"
MIDDLE_MILE_STATE_VALUE11 = "Georgia"
MIDDLE_MILE_STATE_VALUE12 = "District of Columbia"
MIDDLE_MILE_STATE_VALUE13 = "Virginia"
MIDDLE_MILE_STATE_VALUE14 = "Minnesota"
MIDDLE_MILE_STATE_VALUE15 = "Iowa"
MIDDLE_MILE_STATE_VALUE16 = "Nebraska"

RITTER_LENS_COUNTY_VALUE = "Missouri ( MO )"

#############################################################################
SEARCH_COUNTY_VALUE_BEAD = "Autauga County, AL"
SEARCH_COUNTY_VALUE_DCL = "Pima County, AZ"
SEARCH_COUNTY_VALUE_TB= "Blaine County, ID"
SEARCH_COUNTY_VALUE_HOA = "Marshall County, AL"
SEARCH_COUNTY_VALUE_RITTER = "Tennessee ( TN )"
SEARCH_COUNTY_VALUE_PB = "Macon County, AL"
SEARCH_COUNTY_VALUE_LCP = "Houston County, AL"
SEARCH_COUNTY_VALUE_KIN = "Berrien County, GA"
CABLE_ONE_AOI = "Waller_Area 1 (49),Waller-TX"
CABLE_ONE_NETWORK_VALUE = "BFT West"


KINETIC_COUNTY_VALUE = 'Terrell County, GA'


#ritter

TOGGLE_ON_ASSEMBLY_DISTRICT = "State Leg. Dists(L)"
TOGGLE_ON_STATE_SENATE = "State Leg. Dists(U)"
Cordinates = "36.18503743353793, -115.12989093193059"

COUNTY_NAME_AB = "Kings County, NY"

CABINET_CAPACITY = "120"
FLOWERPOT_CAPACITY = "2"
ADJACENT_LOCATIONS = "300"
DROPLINE_LENGTH = "400"
OLT_LATITUDE = "29.654552393024648"
OLT_LONGITUDE = "-82.33334799742548"
