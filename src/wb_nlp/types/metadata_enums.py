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


class GeographicRegions(enum.Enum):
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


class AdminRegions(enum.Enum):
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


class DocTypes(enum.Enum):
    '''Curated list of document types.
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
