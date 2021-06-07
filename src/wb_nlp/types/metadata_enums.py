"""This module contains the curated list of values found in the
WB docs API as well as other constants used in the metadata fields.
"""
import abc
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


class WBEnum(enum.Enum):

    @classmethod
    @abc.abstractmethod
    def clean(cls, value):
        """This method allows us to perform cleaning of the metadata.
        """
        return

    @classmethod
    def _missing_(cls, value):
        """Use the `clean` method to perform the normalization of input values.
        """
        enum_values = set(e.value for e in cls)

        value = cls.clean(value)

        if value not in enum_values:
            raise ValueError("%r is not a valid %s" % (value, cls.__name__))

        return cls(value)


class Corpus(WBEnum):
    ADB = "ADB"
    AFDB = "AFDB"
    ECLAC = "ECLAC"
    EPDC = "EPDC"
    ESCAP = "ESCAP"
    FAO = "FAO"
    IADB = "IADB"
    IIEP = "IIEP"
    IMF = "IMF"
    OECD = "OECD"
    UNECA = "UNECA"
    UNESCWA = "UNESCWA"
    UNHCR = "UNHCR"
    UNIDO = "UNIDO"
    UNODC = "UNODC"
    UNPD = "UNPD"
    WFP = "WFP"
    WB = "WB"

    @classmethod
    def clean(cls, value):
        value = value.upper()

        mappings = {
            "IDB": "IADB",
        }

        value = mappings.get(value, value)

        return value


class WBGeographicRegions(WBEnum):
    '''Curated list of geographic regions.

    delimiter = "|"

    TODO: For further review

    {'': 130220,
    'Latin America & Caribbean': 3992,
    'East Asia and Pacific': 4320,
    'South Eastern Europe and Balkans': 6332,
    'Middle East and North Africa': 3559}

    '''
    # Manually defined
    EMPTY = ""
    latin_america_and_caribbean = "Latin America and Caribbean"
    east_asia_and_pacific = "East Asia and Pacific"
    south_eastern_europe_and_balkans = "South Eastern Europe and Balkans"
    middle_east_and_north_africa = "Middle East and North Africa"

    # From WB docs API curated list
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

    @classmethod
    def clean(cls, value):
        mappings = {
            "latin america & caribbean": "Latin America and Caribbean",
            "africa west": "West Africa",
            None: "",
        }

        value = mappings.get(value.lower(), value)

        return value


class WBAdminRegions(WBEnum):
    '''Curated list of administrative regions.

    delimiter = ","

    TODO: For further review

    {'': 14150, 'OTHER': 1}

    '''
    # Manually defined
    EMPTY = ""

    # From WB docs API curated list
    africa = "Africa"
    africa_east = "Africa East"
    africa_west = "Africa West"
    east_asia_and_pacific = "East Asia and Pacific"
    europe_and_central_asia = "Europe and Central Asia"
    latin_america_and_caribbean = "Latin America and Caribbean"
    middle_east_and_north_africa = "Middle East and North Africa"
    # oth = "OTH"
    # other = "Other"
    others = "Others"
    rest_of_the_world = "Rest Of The World"
    south_asia = "South Asia"
    the_world_region = "The World Region"

    @classmethod
    def clean(cls, value):

        mappings = {
            "latin america & caribbean": "Latin America and Caribbean",
            "latin america &amp; caribbean": "Latin America and Caribbean",
            "oth": "Others",
            "other": "Others",
            None: "",
        }

        value = mappings.get(value.lower(), value)

        return value


class WBDocTypes(WBEnum):
    '''Curated list of document types.

    delimiter = ","

    TODO: For further review

    {'': 15819,
    'Financial Sector Assessment Program (FSAP)': 146,
    'Auditing Document,Financial Monitoring Report,Memorandum,Letter': 138,
    'IEG Approach Paper': 122,
    'Investment Climate Assessment (ICA)': 103,
    'Economic Updates and Modeling': 103,
    'Energy Study': 102,
    'Other Education Study': 83,
    'Inspection Panel Notice of Registration': 79,
    'General Economy, Macroeconomics and Growth Study': 78,
    'Safeguards Diagnostic Review': 72,
    'Interim Strategy Note': 71,
    'World Development Indicators': 65,
    'Country Financial Accountability Assessment': 64,
    'Corporate Governance Assessment (ROSC)': 63,
    'Social Analysis': 62,
    'Other Rural Study': 59,
    'Foreign Trade, FDI, and Capital Flows Study': 58,
    'Country Procurement Assessment (CPAR)': 56,
    'Other Urban Study': 56,
    'GEF Project Brief': 55,
    'Development Policy Review (DPR)': 52,
    'Country Environmental Analysis (CEA)': 52,
    'Integrative Fiduciary Assessment': 52,
    'Education Sector Review': 49,
    'Manual': 47,
    'Investigation Report': 45,
    'Health Sector Review': 42,
    'Sector or Thematic Evaluation': 42,
    'Tranche Release Document': 41,
    'Country Assistance Evaluation': 40,
    'Commodity Working Paper': 40,
    'Program-for-Results Fiduciary Systems Assessment': 39,
    'PSD, Privatization and Industrial Policy': 38,
    'Program-for-Results Technical Assessment': 38,
    'Mining/Oil and Gas': 33,
    'Water & Sanitation Discussion Paper': 31,
    'Country Partnership Framework': 31,
    'Knowledge Economy Study': 29,
    'Global Development Finance - formerly World Debt Tables': 28,
    'Other Financial Accountability Study': 28,
    'City Development Strategy (CDS)': 27,
    'Institutional and Governance Review (IGR)': 27,
    'Country Gender Assessment (CGA)': 26,
    'Internal Discussion Paper': 26,
    'Environment Working Paper': 23,
    'Memorandum & Recommendation of the Director': 22,
    'Global Environment Facility Working Paper': 20,
    'Corporate Evaluation': 19,

    'Women in Development and Gender Study': 19,
    'Rural Development Assessment': 19,
    'Risk and Vulnerability Assessment': 17,
    "Governor's Statement": 17,
    'Memorandum,Financial Monitoring Report,Letter,Auditing Document': 16,
    'LAC Human & Social Development Group Paper Series': 16,
    'Memorandum & Recommendation of the Managing Director': 16,
    'Project Appraisal Document Data Sheet': 15,
    'Strategic Environmental Assessment/Analysis': 14,
    'Legal and Judicial Sector Assessment': 13,
    'Energy-Environment Review': 13,
    'Policy Paper': 13,
    'Country Portfolio Performance Review': 13,
    'Law and Justice Study': 13,
    'Impact Evaluation Report': 13,
    'Country Infrastructure Framework': 12,
    'Report on the World Bank Research Program': 12,
    'Country Engagement Note': 12,
    'Completion Point Document': 11,
    'Other Procurement Study': 10,
    'Commodities Study': 10,
    'GEF Project Document': 10,
    'Preliminary Decision Point Document': 9,
    'Insolvency Assessment (ROSC)': 9,
    'Annual Report on Portfolio Performance': 7,
    'Public Investment Review': 7,
    'Deliverable Document': 7,
    'Transitional Support Strategy': 6,
    'Memorandum &amp; Recommendation of the President': 6,
    'Directory': 5,
    'Country Re-engagement Note': 5,
    'Environmental and Social Framework': 5,
    'Financial Flows': 4,
    'World Bank Atlas': 4,
    'Debt and Creditworthiness Study': 4,
    'Financial Assessment': 4,
    'Price Prospects for Major Primary Commodities': 4,
    'Legal Opinion': 3,
    'Environmental Action Plan': 3,
    'Memorandum,Agreement': 3,
    'Human Capital Working Paper': 3,
    'President&apos;s Report': 3,
    'Decision Point Document': 2,
    'CAS Public Information Note': 2,
    'Project Concept Note': 2,
    'P4R-AF-DRFT-ESSA': 2,
    'Social Action Plan': 2,
    'Environmental Action Plan,Social Action Plan': 2,
    "Managing Director's Report": 2,
    'Public Environmental Expenditure Review (PEER)': 1,
    'Poverty & Social Policy Working Paper': 1,
    'Economic Report': 1,
    'Memorandum,Financial Monitoring Report,Auditing Document,Letter': 1,
    'Auditing/Financial Management,Auditing Document': 1,
    'RP-SP-FULL': 1,
    'Guideline': 1,
    'PROJ-PAP-SP': 1,
    'Issues Paper': 1,
    'The Environmental and Social Review Summary': 1,
    'DRFT-ENV-ASMT-SHP': 1,
    'P4R-AF-APP-PID': 1,
    'Financial Statement,Auditing Document': 1,
    'P4R-AF-FIN-ESSA': 1,
    'Disclosable Project Appraisal Document (PAD)': 1,
    'MADIA Discussion Paper': 1,
    'Recent Economic Developments in Infrastructure (REDI)': 1}
    '''

    # Manually defined
    EMPTY = ""
    annual_report_on_portfolio_performance = "Annual Report on Portfolio Performance"
    auditing_financial_management = "Auditing/Financial Management"
    cas_public_information_note = "CAS Public Information Note"
    city_development_strategy = "City Development Strategy"
    commodities_study = "Commodities Study"
    commodity_working_paper = "Commodity Working Paper"
    completion_point_document = "Completion Point Document"
    corporate_evaluation = "Corporate Evaluation"
    corporate_governance_assessment = "Corporate Governance Assessment"
    country_assistance_evaluation = "Country Assistance Evaluation"
    country_engagement_note = "Country Engagement Note"
    country_environmental_analysis = "Country Environmental Analysis"
    country_financial_accountability_assessment = "Country Financial Accountability Assessment"
    country_gender_assessment = "Country Gender Assessment"
    country_infrastructure_framework = "Country Infrastructure Framework"
    country_partnership_framework = "Country Partnership Framework"
    country_portfolio_performance_review = "Country Portfolio Performance Review"
    country_procurement_assessment = "Country Procurement Assessment"
    country_reengagement_note = "Country Re-engagement Note"
    dataset = "Dataset"
    debt_and_creditworthiness_study = "Debt and Creditworthiness Study"
    decision_point_document = "Decision Point Document"
    deliverable_document = "Deliverable Document"
    development_policy_review = "Development Policy Review"
    directory = "Directory"
    disclosable_project_appraisal_document = "Disclosable Project Appraisal Document"
    drft_env_asmt_shp = "DRFT-ENV-ASMT-SHP"
    economic_report = "Economic Report"
    economic_updates_and_modeling = "Economic Updates and Modeling"
    education_sector_review = "Education Sector Review"
    energy_environment_review = "Energy-Environment Review"
    energy_study = "Energy Study"
    environment_working_paper = "Environment Working Paper"
    environmental_action_plan = "Environmental Action Plan"
    environmental_and_social_framework = "Environmental and Social Framework"
    environmental_and_social_management_framework = "Environmental and Social Management Framework"
    flash_report = "Flash Report"
    financial_assessment = "Financial Assessment"
    financial_flows = "Financial Flows"
    financial_sector_assessment_program = "Financial Sector Assessment Program"
    foreign_trade_fdi_and_capital_flows_study = "Foreign Trade; FDI; and Capital Flows Study"
    gef_project_brief = "GEF Project Brief"
    gef_project_document = "GEF Project Document"
    general_economy_macroeconomics_and_growth_study = "General Economy; Macroeconomics and Growth Study"
    global_development_finance_formerly_world_debt_tables = "Global Development Finance - formerly World Debt Tables"
    global_environment_facility_working_paper = "Global Environment Facility Working Paper"
    governors_statement = "Governor's Statement"
    guideline = "Guideline"
    health_sector_review = "Health Sector Review"
    human_capital_working_paper = "Human Capital Working Paper"
    ieg_approach_paper = "IEG Approach Paper"
    ieg_evaluation = "IEG Evaluation"
    impact_evaluation_report = "Impact Evaluation Report"
    insolvency_assessment = "Insolvency Assessment"
    inspection_panel_notice_of_registration = "Inspection Panel Notice of Registration"
    institutional_and_governance_review = "Institutional and Governance Review"
    integrative_fiduciary_assessment = "Integrative Fiduciary Assessment"
    interim_strategy_note = "Interim Strategy Note"
    internal_discussion_paper = "Internal Discussion Paper"
    investigation_report = "Investigation Report"
    investment_climate_assessment = "Investment Climate Assessment"
    issues_paper = "Issues Paper"
    knowledge_economy_study = "Knowledge Economy Study"
    lac_human_and_social_development_group_paper_series = "LAC Human and Social Development Group Paper Series"
    law_and_justice_study = "Law and Justice Study"
    legal_and_judicial_sector_assessment = "Legal and Judicial Sector Assessment"
    legal_opinion = "Legal Opinion"
    madia_discussion_paper = "MADIA Discussion Paper"
    managing_directors_report = "Managing Director's Report"
    manual = "Manual"
    memorandum_and_recommendation_of_the_director = "Memorandum and Recommendation of the Director"
    memorandum_and_recommendation_of_the_managing_director = "Memorandum and Recommendation of the Managing Director"
    mining_oil_and_gas = "Mining/Oil and Gas"
    other_education_study = "Other Education Study"
    other_financial_accountability_study = "Other Financial Accountability Study"
    other_procurement_study = "Other Procurement Study"
    other_rural_study = "Other Rural Study"
    other_urban_study = "Other Urban Study"
    p_r_af_app_pid = "P4R-AF-APP-PID"
    p_r_af_drft_essa = "P4R-AF-DRFT-ESSA"
    p_r_af_fin_essa = "P4R-AF-FIN-ESSA"
    pas_research_paper = "PAS Research Paper"
    policy = "Policy"
    policy_paper = "Policy Paper"
    poverty_and_social_policy_working_paper = "Poverty and Social Policy Working Paper"
    preliminary_decision_point_document = "Preliminary Decision Point Document"
    presentation = "Presentation"
    price_prospects_for_major_primary_commodities = "Price Prospects for Major Primary Commodities"
    proceedings = "Proceedings"
    procurement_assessment = "Procurement Assessment"
    program_for_results_fiduciary_systems_assessment = "Program-for-Results Fiduciary Systems Assessment"
    program_for_results_technical_assessment = "Program-for-Results Technical Assessment"
    proj_pap_sp = "PROJ-PAP-SP"
    project_appraisal_document_data_sheet = "Project Appraisal Document Data Sheet"
    project_concept_note = "Project Concept Note"
    psd_privatization_and_industrial_policy = "PSD; Privatization and Industrial Policy"
    public_environmental_expenditure_review = "Public Environmental Expenditure Review"
    public_investment_review = "Public Investment Review"
    recent_economic_developments_in_infrastructure = "Recent Economic Developments in Infrastructure"
    reference_material = "Reference Material"
    report_on_the_world_bank_research_program = "Report on the World Bank Research Program"
    risk_and_vulnerability_assessment = "Risk and Vulnerability Assessment"
    rp_sp_full = "RP-SP-FULL"
    rural_development_assessment = "Rural Development Assessment"
    safeguards_diagnostic_review = "Safeguards Diagnostic Review"
    sector_report = "Sector Report"
    sector_or_thematic_evaluation = "Sector or Thematic Evaluation"
    social_action_plan = "Social Action Plan"
    social_analysis = "Social Analysis"
    strategic_environmental_assessment_analysis = "Strategic Environmental Assessment/Analysis"
    supervision_report = "Supervision Report"
    technical_assessment = "Technical Assessment"
    the_environmental_and_social_review_summary = "The Environmental and Social Review Summary"
    tranche_release_document = "Tranche Release Document"
    transitional_support_strategy = "Transitional Support Strategy"
    water_and_sanitation_discussion_paper = "Water and Sanitation Discussion Paper"
    women_in_development_and_gender_study = "Women in Development and Gender Study"
    world_bank_atlas = "World Bank Atlas"
    world_development_indicators = "World Development Indicators"

    # From WB docs API curated list
    # _ = "0"
    accounting_and_auditing_assessment = "Accounting and Auditing Assessment"
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
    executive_directors_statement = "Executive Director's Statement"
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
    memorandum_and_recommendation_of_the_president = "Memorandum and Recommendation of the President"
    minutes = "Minutes"
    monthly_operational_summary = "Monthly Operational Summary"
    news_story = "News Story"
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
    poverty_reduction_strategy_paper = "Poverty Reduction Strategy Paper"
    pre_economic_or_sector_report = "Pre-2003 Economic or Sector Report"
    presidents_report = "President's Report"
    presidents_speech = "President's Speech"
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

    @ classmethod
    def clean(cls, value):
        if value.strip().startswith("Implementation Status and Results Report"):
            value = "Implementation Status and Results Report"
        elif value.strip().startswith("Project Paper"):
            value = "Project Paper"

        mappings = {
            "Financial Sector Assessment Program (FSAP)": "Financial Sector Assessment Program",
            "Investment Climate Assessment (ICA)": "Investment Climate Assessment",
            "Corporate Governance Assessment (ROSC)": "Corporate Governance Assessment",
            "Foreign Trade, FDI, and Capital Flows Study": "Foreign Trade; FDI; and Capital Flows Study",
            "Country Procurement Assessment (CPAR)": "Country Procurement Assessment",
            "Development Policy Review (DPR)": "Development Policy Review",
            "Country Environmental Analysis (CEA)": "Country Environmental Analysis",
            "Water & Sanitation Discussion Paper": "Water and Sanitation Discussion Paper",
            "City Development Strategy (CDS)": "City Development Strategy",
            "Institutional and Governance Review (IGR)": "Institutional and Governance Review",
            "Country Gender Assessment (CGA)": "Country Gender Assessment",
            "Memorandum & Recommendation of the Director": "Memorandum and Recommendation of the Director",
            "LAC Human & Social Development Group Paper Series": "LAC Human and Social Development Group Paper Series",
            "Memorandum & Recommendation of the Managing Director": "Memorandum and Recommendation of the Managing Director",
            "Insolvency Assessment (ROSC)": "Insolvency Assessment",
            "Memorandum &amp; Recommendation of the President": "Memorandum and Recommendation of the President",
            "President&apos;s Report": "President's Report",
            "Public Environmental Expenditure Review (PEER)": "Public Environmental Expenditure Review",
            "Poverty & Social Policy Working Paper": "Poverty and Social Policy Working Paper",
            "Disclosable Project Appraisal Document (PAD)": "Disclosable Project Appraisal Document",
            "Recent Economic Developments in Infrastructure (REDI)": "Recent Economic Developments in Infrastructure",
            "General Economy, Macroeconomics and Growth Study": "General Economy; Macroeconomics and Growth Study",
            "PSD, Privatization and Industrial Policy": "PSD; Privatization and Industrial Policy",

            # Cleaning doc type from WB API
            "Accounting and Auditing Assessment (ROSC)": "Accounting and Auditing Assessment",
            "Memorandum & Recommendation of the President": "Memorandum and Recommendation of the President",
            "Poverty Reduction Strategy Paper (PRSP)": "Poverty Reduction Strategy Paper",

            None: "",
        }

        value = mappings.get(value, value)

        return value


class WBMajorDocTypes(WBEnum):
    '''Curated list of major document types.

    TODO: For further review

    {'': 14158}

    '''
    # Manually defined
    EMPTY = ""

    # From WB docs API curated list
    board_documents = "Board Documents"
    country_focus = "Country Focus"
    economic_and_sector_work = "Economic and Sector Work"
    # economic_sector_work = "Economic & Sector Work"
    # economic_amp_sector_work = "Economic &amp; Sector Work"
    project_documents = "Project Documents"
    # publications = "Publications"
    publications_and_research = "Publications and Research"
    # publications_research = "Publications & Research"
    # publications_amp_research = "Publications &amp; Research"

    @ classmethod
    def clean(cls, value):

        mappings = {
            "Publication": "Publications and Research",
            "Publications": "Publications and Research",
            "Publications & Research": "Publications and Research",
            "Publications &amp; Research": "Publications and Research",
            "Economic & Sector Work": "Economic and Sector Work",
            "Economic &amp; Sector Work": "Economic and Sector Work",
            None: "",
        }

        value = mappings.get(value, value)

        return value


class MajorDocTypes(WBEnum):
    '''
    Curated list of major document types.
    Document types are adapted from various sources as needed.
    '''
    EMPTY = ""

    # From ADB
    evaluation_document = "Evaluation Document"

    # From WB docs API curated list
    board_documents = "Board Documents"
    country_focus = "Country Focus"
    economic_and_sector_work = "Economic and Sector Work"
    project_documents = "Project Documents"
    publications_and_research = "Publications and Research"

    @ classmethod
    def clean(cls, value):

        mappings = {
            "Publication": "Publications and Research",
            "Publications": "Publications and Research",
            "Publications & Research": "Publications and Research",
            "Publications &amp; Research": "Publications and Research",

            "Economic & Sector Work": "Economic and Sector Work",
            "Economic &amp; Sector Work": "Economic and Sector Work",

            "Project Document": "Project Documents",
            None: "",
        }

        value = mappings.get(value, value)

        return value


class WBTopics(enum.Enum):
    '''Curated list of topics.

    NOTE: What is this??? https://vocabulary.worldbank.org/PoolParty/sparql/taxonomy

    PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
    SELECT DISTINCT ?Concept ?prefLabel
    WHERE
    { ?Concept ?x skos:Concept .
    { ?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '.*', 'i'))  }
    } ORDER BY ?prefLabel


    PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
    SELECT DISTINCT ?Concept ?altLabel
    WHERE
    { ?Concept ?x skos:Concept .
    { ?Concept skos:altLabel ?altLabel . FILTER (regex(str(?altLabel), '.*', 'i'))  }
    } ORDER BY ?altLabel


    delimiter = ","

    TODO: For further review

    d = d.replace("Health, Nutrition and Population",
                "Health; Nutrition and Population")

    {'': 68000}

    '''
    # Manually defined
    EMPTY = ""

    # From WB docs API curated list
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
    # international_economics_trade = "International Economics & Trade"
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

    @ classmethod
    def clean(cls, value):

        mappings = {
            "Health, Nutrition and Population": "Health; Nutrition and Population",
            "International Economics & Trade": "International Economics and Trade",
            None: "",
        }

        value = mappings.get(value, value)

        return value


# class WBSubTopics(enum.Enum):
#     '''Curated list of sub-topics.
#     '''
#     access_of_poor_to_social_services = "Access of Poor to Social Services"
#     agricultural_growth_and_rural_development = "Agricultural Growth and Rural Development"
#     bankruptcy_and_resolution_of_financial_distress = "Bankruptcy and Resolution of Financial Distress"
#     banks_banking_reform = "Banks & Banking Reform"
#     brown_issues_and_health = "Brown Issues and Health"
#     business_cycles_and_stabilization_policies = "Business Cycles and Stabilization Policies"
#     climate_change_mitigation_and_green_house_gases = "Climate Change Mitigation and Green House Gases"
#     climate_change_and_agriculture = "Climate Change and Agriculture"
#     coastal_and_marine_resources = "Coastal and Marine Resources"
#     common_carriers_industry = "Common Carriers Industry"
#     communicable_diseases = "Communicable Diseases"
#     construction_industry = "Construction Industry"
#     crops_and_crop_management_systems = "Crops and Crop Management Systems"
#     de_facto_governments = "De Facto Governments"
#     debt_markets = "Debt Markets"
#     democratic_government = "Democratic Government"
#     disability = "Disability"
#     disease_control_prevention = "Disease Control & Prevention"
#     economic_adjustment_and_lending = "Economic Adjustment and Lending"
#     economic_assistance = "Economic Assistance"
#     economic_growth = "Economic Growth"
#     economic_theory_research = "Economic Theory & Research"
#     economics_and_finance_of_public_institution_development = "Economics and Finance of Public Institution Development"
#     education_for_all = "Education For All"
#     educational_institutions_facilities = "Educational Institutions & Facilities"
#     educational_sciences = "Educational Sciences"
#     effective_schools_and_teachers = "Effective Schools and Teachers"
#     energy_demand = "Energy Demand"
#     energy_policies_economics = "Energy Policies & Economics"
#     energy_and_environment = "Energy and Environment"
#     energy_and_mining = "Energy and Mining"
#     energy_and_natural_resources = "Energy and Natural Resources"
#     engineering = "Engineering"
#     environmental_engineering = "Environmental Engineering"
#     environmental_protection = "Environmental Protection"
#     financial_sector_policy = "Financial Sector Policy"
#     food_beverage_industry = "Food & Beverage Industry"
#     food_security = "Food Security"
#     gender_and_development = "Gender and Development"
#     general_manufacturing = "General Manufacturing"
#     global_environment = "Global Environment"
#     government_policies = "Government Policies"
#     health_care_services_industry = "Health Care Services Industry"
#     health_service_management_and_delivery = "Health Service Management and Delivery"
#     health_and_sanitation = "Health and Sanitation"
#     hydrology = "Hydrology"
#     industrial_economics = "Industrial Economics"
#     inequality = "Inequality"
#     inflation = "Inflation"
#     information_technology = "Information Technology"
#     intelligent_transport_systems = "Intelligent Transport Systems"
#     international_trade_and_trade_rules = "International Trade and Trade Rules"
#     judicial_system_reform = "Judicial System Reform"
#     labor_markets = "Labor Markets"
#     legal_products = "Legal Products"
#     legal_reform = "Legal Reform"
#     legislation = "Legislation"
#     livestock_and_animal_husbandry = "Livestock and Animal Husbandry"
#     macro_fiscal_policy = "Macro-Fiscal Policy"
#     macroeconomic_management = "Macroeconomic Management"
#     marketing = "Marketing"
#     microfinance = "Microfinance"
#     municipal_management_and_reform = "Municipal Management and Reform"
#     national_governance = "National Governance"
#     natural_disasters = "Natural Disasters"
#     nutrition = "Nutrition"
#     plastics_rubber_industry = "Plastics & Rubber Industry"
#     pollution_management_control = "Pollution Management & Control"
#     post_conflict_reconstruction = "Post Conflict Reconstruction"
#     private_sector_development_law = "Private Sector Development Law"
#     private_sector_economics = "Private Sector Economics"
#     public_finance_decentralization_and_poverty_reduction = "Public Finance Decentralization and Poverty Reduction"
#     public_health_promotion = "Public Health Promotion"
#     public_sector_administrative_civil_service_reform = "Public Sector Administrative & Civil Service Reform"
#     public_sector_administrative_and_civil_service_reform = "Public Sector Administrative and Civil Service Reform"
#     public_sector_corruption_anticorruption_measures = "Public Sector Corruption & Anticorruption Measures"
#     public_sector_economics = "Public Sector Economics"
#     pulp_paper_industry = "Pulp & Paper Industry"
#     regulatory_regimes = "Regulatory Regimes"
#     renewable_energy = "Renewable Energy"
#     roads_highways = "Roads & Highways"
#     rural_labor_markets = "Rural Labor Markets"
#     rural_settlements = "Rural Settlements"
#     rural_and_renewable_energy = "Rural and Renewable Energy"
#     sanitary_environmental_engineering = "Sanitary Environmental Engineering"
#     sanitation_and_sewerage = "Sanitation and Sewerage"
#     services_transfers_to_poor = "Services & Transfers to Poor"
#     small_private_water_supply_providers = "Small Private Water Supply Providers"
#     social_assessment = "Social Assessment"
#     social_policy = "Social Policy"
#     state_owned_enterprise_reform = "State Owned Enterprise Reform"
#     town_water_supply_and_sanitation = "Town Water Supply and Sanitation"
#     transport_services = "Transport Services"
#     urban_governance_and_management = "Urban Governance and Management"
#     urban_housing = "Urban Housing"
#     urban_housing_and_land_settlements = "Urban Housing and Land Settlements"
#     water_supply_and_sanitation_economics = "Water Supply and Sanitation Economics"
#     water_and_food_supply = "Water and Food Supply"
#     water_and_human_health = "Water and Human Health"
#     youth_and_governance = "Youth and Governance"


WBGeographicRegions.delimiter = "|"
WBAdminRegions.delimiter = ","
WBDocTypes.delimiter = ","
WBMajorDocTypes.delimiter = ","
WBTopics.delimiter = ","
