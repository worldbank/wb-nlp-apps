"""This module contains the curated list of values found in the
WB docs API as well as other constants used in the metadata fields.
"""
import enum
import re
import requests
from bs4 import BeautifulSoup


def get_wb_curated_list(list_id):
    """Enumerates the list of items corresponding to the given `list_id` found in the
    World Bank's wds API.

    Source: https://search.worldbank.org/api/v2/wds

    Example:
        list_id = "geo_reg"
    """
    r = requests.get('https://search.worldbank.org/api/v2/wds')
    b = BeautifulSoup(r.content, 'html.parser')

    item_list = b.find('select', id=list_id).find_all('option')
    g = {re.sub(r'[^a-z]+', '_', o.text.lower()).strip('_')
                : o.text for o in item_list}

    for k, v in g.items():
        print(f'{k} = "{v}"')


class Corpus(enum.Enum):
    adb = "ADB"
    afdb = "AFDB"
    eclac = "ECLAC"
    epdc = "EPDC"
    escap = "ESCAP"
    fao = "FAO"
    idb = "IDB"
    iiep = "IIEP"
    oecd = "OECD"
    uneca = "UNECA"
    unescwa = "UNESCWA"
    unhcr = "UNHCR"
    unido = "UNIDO"
    unodc = "UNODC"
    unpd = "UNPD"
    wfp = "WFP"
    wb = "WB"


class WBGeographicRegions(enum.Enum):
    '''Curated list of geographic regions.
    '''
    africa = "Africa"
    america = "America"
    asia = "Asia"
    caribbean = "Caribbean"
    central_africa = "Central Africa"
    central_america = "Central America"
    central_asia = "Central Asia"
    commonwealth_of_independent_states = "Commonwealth of Independent States"
    east_africa = "East Africa"
    east_asia = "East Asia"
    eastern_europe = "Eastern Europe"
    europe = "Europe"
    europe_and_central_asia = "Europe and Central Asia"
    europe_middle_east_and_north_africa = "Europe, Middle East and North Africa"
    european_union = "European Union"
    latin_america = "Latin America"
    middle_east = "Middle East"
    north_africa = "North Africa"
    north_america = "North America"
    oceania = "Oceania"
    sahel = "Sahel"
    south_america = "South America"
    south_asia = "South Asia"
    southeast_asia = "Southeast Asia"
    southern_africa = "Southern Africa"
    sub_saharan_africa = "Sub-Saharan Africa"
    west_africa = "West Africa"
    world = "World"


class WBAdminRegions(enum.Enum):
    '''Curated list of administrative regions.
    '''
    africa = "Africa"
    africa_east = "Africa East"
    africa_west = "Africa West"
    east_asia_and_pacific = "East Asia and Pacific"
    europe_and_central_asia = "Europe and Central Asia"
    latin_america_caribbean = "Latin America & Caribbean"
    latin_america_amp_caribbean = "Latin America &amp; Caribbean"
    middle_east_and_north_africa = "Middle East and North Africa"
    oth = "OTH"
    other = "Other"
    others = "Others"
    rest_of_the_world = "Rest Of The World"
    south_asia = "South Asia"
    the_world_region = "The World Region"


class WBDocTypes(enum.Enum):
    '''Curated list of document types.

    For further review:

    Counter({'General Economy, Macroeconomics and Growth Study': 78,
            'Foreign Trade, FDI, and Capital Flows Study': 58,
            'PSD, Privatization and Industrial Policy': 38,
            'Auditing Document,Financial Monitoring Report,Memorandum,Letter': 138,
            'Memorandum,Financial Monitoring Report,Letter,Auditing Document': 16,
            'Memorandum,Financial Monitoring Report,Auditing Document,Letter': 1,
            'Auditing/Financial Management,Auditing Document': 1,
            'Implementation Status and Results ReportEthiopia Water Supply, Sanitation and Hygiene Project': 1,
            'Implementation Status and Results ReportServing People, Improving Health Project': 1,
            'Project PaperSwaziland Health, HIV/AIDS and TB Project': 1,
            'Implementation Status and Results ReportGhana - Maternal, Child Health and Nutrition Project': 1,
            'Implementation Status and Results ReportLAKE VICTORIA TRANSPORT PROGRAM - SOP1, RWANDA': 1,
            'Financial Statement,Auditing Document': 1,
            'Memorandum,Agreement': 3,
            'Environmental Action Plan,Social Action Plan': 2})
    '''
    # _ = "0"
    accounting_and_auditing_assessment_rosc = "Accounting and Auditing Assessment (ROSC)"
    agenda = "Agenda"
    agreement = "Agreement"
    aide_memoire = "Aide Memoire"
    announcement = "Announcement"
    annual_report = "Annual Report"
    audit = "Audit"
    auditing_document = "Auditing Document"
    board_report = "Board Report"
    board_summary = "Board Summary"
    brief = "Brief"
    cas_completion_report_review = "CAS Completion Report Review"
    cas_progress_report = "CAS Progress Report"
    correspondence = "Correspondence"
    country_assistance_strategy_document = "Country Assistance Strategy Document"
    country_economic_memorandum = "Country Economic Memorandum"
    credit_agreement = "Credit Agreement"
    departmental_working_paper = "Departmental Working Paper"
    disbursement_letter = "Disbursement Letter"
    esmap_paper = "ESMAP Paper"
    environmental_assessment = "Environmental Assessment"
    environmental_and_social_assessment = "Environmental and Social Assessment"
    environmental_and_social_commitment_plan = "Environmental and Social Commitment Plan"
    environmental_and_social_management_plan = "Environmental and Social Management Plan"
    environmental_and_social_review_summary = "Environmental and Social Review Summary"
    executive_director_s_statement = "Executive Director's Statement"
    financial_monitoring_report = "Financial Monitoring Report"
    financial_statement = "Financial Statement"
    financing_agreement = "Financing Agreement"
    funding_proposal = "Funding Proposal"
    grant_or_trust_fund_agreement = "Grant or Trust Fund Agreement"
    guarantee_agreement = "Guarantee Agreement"
    implementation_completion_report_review = "Implementation Completion Report Review"
    implementation_completion_and_results_report = "Implementation Completion and Results Report"
    implementation_status_and_results_report = "Implementation Status and Results Report"
    indigenous_peoples_plan = "Indigenous Peoples Plan"
    information_notice = "Information Notice"
    inspection_panel_report_and_recommendation = "Inspection Panel Report and Recommendation"
    integrated_safeguards_data_sheet = "Integrated Safeguards Data Sheet"
    journal_article = "Journal Article"
    letter = "Letter"
    letter_of_development_policy = "Letter of Development Policy"
    loan_agreement = "Loan Agreement"
    memorandum = "Memorandum"
    memorandum_recommendation_of_the_president = "Memorandum & Recommendation of the President"
    minutes = "Minutes"
    monthly_operational_summary = "Monthly Operational Summary"
    newsletter = "Newsletter"
    note_on_cancelled_operation = "Note on Cancelled Operation"
    other_agricultural_study = "Other Agricultural Study"
    other_environmental_study = "Other Environmental Study"
    other_financial_sector_study = "Other Financial Sector Study"
    other_health_study = "Other Health Study"
    other_infrastructure_study = "Other Infrastructure Study"
    other_poverty_study = "Other Poverty Study"
    other_public_sector_study = "Other Public Sector Study"
    other_social_protection_study = "Other Social Protection Study"
    policy_note = "Policy Note"
    policy_research_working_paper = "Policy Research Working Paper"
    poverty_assessment = "Poverty Assessment"
    poverty_reduction_strategy_paper_prsp = "Poverty Reduction Strategy Paper (PRSP)"
    pre_economic_or_sector_report = "Pre-2003 Economic or Sector Report"
    president_s_report = "President's Report"
    president_s_speech = "President's Speech"
    procedure_and_checklist = "Procedure and Checklist"
    procurement_plan = "Procurement Plan"
    program_document = "Program Document"
    program_information_document = "Program Information Document"
    program_for_results_environmental_and_social_systems_assessment = "Program-for-Results Environmental and Social Systems Assessment"
    project_agreement = "Project Agreement"
    project_appraisal_document = "Project Appraisal Document"
    project_completion_report = "Project Completion Report"
    project_implementation_plan = "Project Implementation Plan"
    project_information_document = "Project Information Document"
    project_information_and_integrated_safeguards_data_sheet = "Project Information and Integrated Safeguards Data Sheet"
    project_paper = "Project Paper"
    project_performance_assessment_report = "Project Performance Assessment Report"
    project_preparation_facility_document = "Project Preparation Facility Document"
    project_status_report = "Project Status Report"
    public_expenditure_review = "Public Expenditure Review"
    publication = "Publication"
    report = "Report"
    resettlement_plan = "Resettlement Plan"
    side_letter = "Side Letter"
    social_assessment = "Social Assessment"
    staff_appraisal_report = "Staff Appraisal Report"
    staff_working_paper = "Staff Working Paper"
    stakeholder_engagement_plan = "Stakeholder Engagement Plan"
    statutory_committee_report = "Statutory Committee Report"
    systematic_country_diagnostic = "Systematic Country Diagnostic"
    technical_annex = "Technical Annex"
    transcript = "Transcript"
    trust_fund_administrative_agreement = "Trust Fund Administrative Agreement"
    viewpoint = "Viewpoint"
    wbi_working_paper = "WBI Working Paper"
    working_paper = "Working Paper"
    working_paper_numbered_series = "Working Paper (Numbered Series)"
    world_bank_annual_report = "World Bank Annual Report"
    world_development_report = "World Development Report"


class WBMajorDocTypes(enum.Enum):
    '''Curated list of major document types.
    '''
    board_documents = "Board Documents"
    country_focus = "Country Focus"
    economic_sector_work = "Economic & Sector Work"
    economic_amp_sector_work = "Economic &amp; Sector Work"
    project_documents = "Project Documents"
    publications = "Publications"
    publications_research = "Publications & Research"
    publications_amp_research = "Publications &amp; Research"


class WBTopics(enum.Enum):
    '''Curated list of topics.
    '''
    agriculture = "Agriculture"
    communities_and_human_settlements = "Communities and Human Settlements"
    conflict_and_development = "Conflict and Development"
    culture_and_development = "Culture and Development"
    education = "Education"
    energy = "Energy"
    environment = "Environment"
    finance_and_financial_sector_development = "Finance and Financial Sector Development"
    gender = "Gender"
    governance = "Governance"
    health_nutrition_and_population = "Health; Nutrition and Population"
    industry = "Industry"
    informatics = "Informatics"
    information_and_communication_technologies = "Information and Communication Technologies"
    infrastructure_economics_and_finance = "Infrastructure Economics and Finance"
    international_economics_trade = "International Economics & Trade"
    international_economics_and_trade = "International Economics and Trade"
    law_and_development = "Law and Development"
    macroeconomics_and_economic_growth = "Macroeconomics and Economic Growth"
    poverty_reduction = "Poverty Reduction"
    private_sector_development = "Private Sector Development"
    public_sector_development = "Public Sector Development"
    rural_development = "Rural Development"
    science_and_technology_development = "Science and Technology Development"
    social_development = "Social Development"
    social_protections_and_labor = "Social Protections and Labor"
    transport = "Transport"
    urban_development = "Urban Development"
    water_resources = "Water Resources"
    water_supply_and_sanitation = "Water Supply and Sanitation"


class WBSubTopics(enum.Enum):
    '''Curated list of sub-topics.
    '''
    access_of_poor_to_social_services = "Access of Poor to Social Services"
    agricultural_growth_and_rural_development = "Agricultural Growth and Rural Development"
    bankruptcy_and_resolution_of_financial_distress = "Bankruptcy and Resolution of Financial Distress"
    banks_banking_reform = "Banks & Banking Reform"
    brown_issues_and_health = "Brown Issues and Health"
    business_cycles_and_stabilization_policies = "Business Cycles and Stabilization Policies"
    climate_change_mitigation_and_green_house_gases = "Climate Change Mitigation and Green House Gases"
    climate_change_and_agriculture = "Climate Change and Agriculture"
    coastal_and_marine_resources = "Coastal and Marine Resources"
    common_carriers_industry = "Common Carriers Industry"
    communicable_diseases = "Communicable Diseases"
    construction_industry = "Construction Industry"
    crops_and_crop_management_systems = "Crops and Crop Management Systems"
    de_facto_governments = "De Facto Governments"
    debt_markets = "Debt Markets"
    democratic_government = "Democratic Government"
    disability = "Disability"
    disease_control_prevention = "Disease Control & Prevention"
    economic_adjustment_and_lending = "Economic Adjustment and Lending"
    economic_assistance = "Economic Assistance"
    economic_growth = "Economic Growth"
    economic_theory_research = "Economic Theory & Research"
    economics_and_finance_of_public_institution_development = "Economics and Finance of Public Institution Development"
    education_for_all = "Education For All"
    educational_institutions_facilities = "Educational Institutions & Facilities"
    educational_sciences = "Educational Sciences"
    effective_schools_and_teachers = "Effective Schools and Teachers"
    energy_demand = "Energy Demand"
    energy_policies_economics = "Energy Policies & Economics"
    energy_and_environment = "Energy and Environment"
    energy_and_mining = "Energy and Mining"
    energy_and_natural_resources = "Energy and Natural Resources"
    engineering = "Engineering"
    environmental_engineering = "Environmental Engineering"
    environmental_protection = "Environmental Protection"
    financial_sector_policy = "Financial Sector Policy"
    food_beverage_industry = "Food & Beverage Industry"
    food_security = "Food Security"
    gender_and_development = "Gender and Development"
    general_manufacturing = "General Manufacturing"
    global_environment = "Global Environment"
    government_policies = "Government Policies"
    health_care_services_industry = "Health Care Services Industry"
    health_service_management_and_delivery = "Health Service Management and Delivery"
    health_and_sanitation = "Health and Sanitation"
    hydrology = "Hydrology"
    industrial_economics = "Industrial Economics"
    inequality = "Inequality"
    inflation = "Inflation"
    information_technology = "Information Technology"
    intelligent_transport_systems = "Intelligent Transport Systems"
    international_trade_and_trade_rules = "International Trade and Trade Rules"
    judicial_system_reform = "Judicial System Reform"
    labor_markets = "Labor Markets"
    legal_products = "Legal Products"
    legal_reform = "Legal Reform"
    legislation = "Legislation"
    livestock_and_animal_husbandry = "Livestock and Animal Husbandry"
    macro_fiscal_policy = "Macro-Fiscal Policy"
    macroeconomic_management = "Macroeconomic Management"
    marketing = "Marketing"
    microfinance = "Microfinance"
    municipal_management_and_reform = "Municipal Management and Reform"
    national_governance = "National Governance"
    natural_disasters = "Natural Disasters"
    nutrition = "Nutrition"
    plastics_rubber_industry = "Plastics & Rubber Industry"
    pollution_management_control = "Pollution Management & Control"
    post_conflict_reconstruction = "Post Conflict Reconstruction"
    private_sector_development_law = "Private Sector Development Law"
    private_sector_economics = "Private Sector Economics"
    public_finance_decentralization_and_poverty_reduction = "Public Finance Decentralization and Poverty Reduction"
    public_health_promotion = "Public Health Promotion"
    public_sector_administrative_civil_service_reform = "Public Sector Administrative & Civil Service Reform"
    public_sector_administrative_and_civil_service_reform = "Public Sector Administrative and Civil Service Reform"
    public_sector_corruption_anticorruption_measures = "Public Sector Corruption & Anticorruption Measures"
    public_sector_economics = "Public Sector Economics"
    pulp_paper_industry = "Pulp & Paper Industry"
    regulatory_regimes = "Regulatory Regimes"
    renewable_energy = "Renewable Energy"
    roads_highways = "Roads & Highways"
    rural_labor_markets = "Rural Labor Markets"
    rural_settlements = "Rural Settlements"
    rural_and_renewable_energy = "Rural and Renewable Energy"
    sanitary_environmental_engineering = "Sanitary Environmental Engineering"
    sanitation_and_sewerage = "Sanitation and Sewerage"
    services_transfers_to_poor = "Services & Transfers to Poor"
    small_private_water_supply_providers = "Small Private Water Supply Providers"
    social_assessment = "Social Assessment"
    social_policy = "Social Policy"
    state_owned_enterprise_reform = "State Owned Enterprise Reform"
    town_water_supply_and_sanitation = "Town Water Supply and Sanitation"
    transport_services = "Transport Services"
    urban_governance_and_management = "Urban Governance and Management"
    urban_housing = "Urban Housing"
    urban_housing_and_land_settlements = "Urban Housing and Land Settlements"
    water_supply_and_sanitation_economics = "Water Supply and Sanitation Economics"
    water_and_food_supply = "Water and Food Supply"
    water_and_human_health = "Water and Human Health"
    youth_and_governance = "Youth and Governance"
