from enum import Enum


class Environment(Enum):
    LOCAL = "local"
    AWS_GLUE = "glue"
    LAMBDA = "lambda"


class CommonColumns(Enum):
    CREATE_AT = "created_at"
    UPDATE_AT = "updated_at"
    CREATE_BY = "created_by"
    UPDATE_BY = "updated_by"
    EFFECTIVE_FROM = "effective_from"
    EFFECTIVE_TO = "effective_to"
    IS_ACTIVE = "is_active"
    RAW_COLUMNS = "raw_columns"
    NEW_COLUMNS = "new_columns"
    TARGET_COLUMNS = "target_columns"
    HASHCODE = "hashcode"


class FileType(Enum):
    """File type

    Args:
        Enum (str): type of input file
    """
    EXCEL = 'excel'
    CSV = 'csv'
    CSV_LOCAL = 'csv_local'
    EXCEL_LOCAL = 'excel_local'
    REDSHIFT = 'redshift'


class ProfiledState(Enum):
    PROFILED = "Profiled"
    NOT_PROFILED = "Not profiled"
    EXCLUDED = "Excluded"


class RiskLevel(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class InherentRiskValue(Enum):
    LOW = "Low Risk"
    MEDIUM = "Med Risk"
    HIGH = "High Risk"


class ControlMeasureValue(Enum):
    STRONG = "Strong"
    ACCEPTABLE = "Acceptable"
    FAIR = "Fair"


class ResidualScoreValue(Enum):
    LOW = "Low Risk"
    MEDIUM = "Medium Risk"
    HIGH = "High Risk"


class SmsCertLevel(Enum):
    BIZ_LV_3 = "bizSAFE Level 3"
    BIZ_LV_4 = "bizSAFE Level 4"
    BIZ_ISO_45001 = "bizSAFE Star / ISO 45001"


class MatrixMappingValue(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    STRONG = "Strong"
    ACCEPTABLE = "Acceptable"
    FAIR = "Fair"
    SUBCONTRACTOR = "subcontractors"
    DEFAULT_COUNT = 0


class ProfileSubContractorColumnState(Enum):
    """Reponse state

    Args:
        Enum (str): type of response state
    """
    YES = 1
    PREV_MONTH_NUM_WORK_DECLARE_STANDARD = 10
    NOT_SUBMITTED = "Not Submitted"
    SUBMITTED = "Submitted"


class ResponseState(Enum):
    """Reponse state

    Args:
        Enum (str): type of response state
    """
    YES = "Y"
    NO = "N"
    NONE = ""
    NULL_VALUE = "NaN"


class Model(Enum):
    SUBCONTRACTOR = "subcontractor"
    WORK_ACTIVITY = "work_activity"
    WORKER = "worker"
    LAMBDA = "lambda"
    CESP = "cesp"


class ModelType(Enum):
    RISK = "risk"
    PROFILING = "profiling"
    INGEST_WDC = "ingest_wdc"
    INGEST_TRAINING_COURSES = "ingest_training_courses"
    INGEST_SURVEY = "ingest_survey"
    INGEST_USER = "ingest_user"
    CESP = "cesp"


class SmsCertLevel(Enum):
    BIZ_LV_3 = "bizSAFE Level 3"
    BIZ_LV_4 = "bizSAFE Level 4"
    BIZ_ISO_45001 = "bizSAFE Star / ISO 45001"


class ProfilingColumns(Enum):
    PACKAGE = "package"
    SUBCONTRACTOR = "subcontractor"
    REMARK = "remark"
    FORWARD_INHERENT_DATA = "did_not_submit_two_months_look_ahead"
    SAFETY_PERFORMANCE_SCORE = "did_not_submit_subcontractor_safety"
    PRE_MONTH_NO_WORK_DECLARED_SCORE = "pre_month_no_work_declared_score"
    PROFILED_STATUS_COLUMN = "profiled_status"
    WORK_DATE = "work_date"
    DATE = "date"
    MONTH = "month"


class SubconRiskColumns(Enum):
    REMARK = "remark"
    PACKAGE = "package"
    SUBCONTRACTOR = "subcontractor"
    NEW_CONTRACTOR = "new_contractor"
    IS_NEW_CONTRACTOR = "is_new_contractor"
    IS_NEW_LOCATION = "is_new_location"
    IS_NEW_ACTIVITY = "is_new_activity"
    IS_NON_ROUTINE_WORK = "is_non_routine_work"
    HIRA = "hira"
    HIRA_SCORE = "hira_score"
    IS_ACCEPTED_MSRA_AND_WORK = "is_accepted_msra_and_work"
    IS_CRITICAL_PATH = "is_critical_path"
    IS_BEHIND_SCHEDULE = "is_behind_schedule"
    IS_COMPLETE_OVER_80 = "is_complete_over_80"
    SCORE_A = "score_a"
    SCORE_B = "score_b"
    SCORE_C = "score_c"
    PROCESS_C = "process_c"
    SCORE_D = "score_d"
    SCORE_D_TMP = "score_d_tmp"
    PROCESS_E = "process_e"
    SCORE_E = "score_e"
    MONTH = "month"
    SMS_CERT = "sms_cert"
    BAND_2 = "band_2"
    LEADERSHIP = "leadership"
    GOVERNANCE = "governance"
    WORK = "work"
    ORGANISATION = "organisation"
    OWNERSHIP_TEAMWORK = "ownership_teamwork"
    COMMUNICATION = "communication"
    SCORE = "score"
    DATE_OF_OBSERVATION = "date_of_observation"
    DATE_OF_OBS = "date_of_obs"
    STATUS = "status"
    SIGNIFICANT_OF_OBS = "significant_of_obs"
    CLASSIFICATION_INCIDENTS = "classification_incidents"
    INHERENT_RISK_GROUP = "inherent_risk_group"
    CONTROL_MEASURE_GROUP = "control_measure_group"
    COUNT = "count"
    INHERENT_SCORE = "inherent_score"
    TOTAL = "total"
    COUNT_OBS = "count_obs"
    COUNT_SIG = "count_sig"
    TOTAL_BY_DISTINCT_DATE = "total_by_distinct_date"
    COUNT_H1 = "count_h1"
    COUNT_H2 = "count_h2"
    COUNT_H3 = "count_h3"
    SCORE_F = "score_f"
    NUM_OF_INSPECS = "num_inspections"
    SCORE_G1 = "score_g1"
    SCORE_G2 = "score_g2"
    SCORE_G_TMP = "score_g_tmp"
    SCORE_G = "score_g"
    NUM_OF_OBS = "num_observations"
    RESULT_H1 = "result_h1"
    RESULT_H2 = "result_h2"
    RESULT_H3 = "result_h3"
    SCORE_H = "score_h"
    SCORE_H_TEMP = "score_h_tmp"
    NUM_OF_INCIDENTS = "num_incidents"
    SCORE_I = "score_i"
    SAFETY_PERFORMANCE = "safety_performance"
    SCORE_J = "score_j"
    SCORE_K = "score_k"
    SCORE_L = "score_l"
    RESIDUAL_SCORE = "residual_score"
    CONTROL_MEASURE_SCORE = "control_measure_score"
    MATRIX_MODEL = "model"
    MATRIX_TYPE_ROW = "type"
    MATRIX_LOW_DATA = "low"
    MATRIX_MEDIUM_DATA = "medium"
    MATRIX_HIGH_DATA = "high"
    PROFILE_RESULT = "profiled_status"
    SMS_CERTIFICATION = "sms_certification"
    UNFAMILIAR_WORK_ACTIVITIY = "unfamiliar_work_activity"
    TIME = "time"
    MAIN_CONTRACTOR_CONSASS = "consass"
    MAIN_CONTRACTOR_SSPA = "sspa"
    MAIN_CONTRACTOR_CULTURE_SAFE = "culturesafe"
    DATE = "date"


class WorkActivityProfiledColumn(Enum):
    WORK_DATE = "work_date"
    PACKAGE = "package"
    WORK_LOCATION = "work_location"
    SUBCONTRACTOR = "subcontractor"
    SUBMITTED_DATE = "submitted_date"
    PROFILED_STATUS = "profiled_status"
    TYPE_OF_WORK_ACTIVITIES = "work_activity"
    DNS_TWO_MONTH_LOOK_AHEAD = "did_not_submit_two_months_look_ahead"
    DNS_SUB_SAFETY = "did_not_submit_subcontractor_safety"
    STATUS = "status"
    CASE_STATUS = "case_status"
    DATE = "date"
    DATETIME = "datetime"
    TIME_RANGE = "time_range"


class WorkActivityRiskColumn(Enum):
    """Column name

    Args:
        Enum (str): type of input file
    """
    REFERENCE_ID = "reference_id"
    WORK_DATE = "work_date"
    PACKAGE = "package"
    WORKING_TIME = "working_time"
    WORK_LOCATION = "work_location"
    WORK_TYPE = "work_type"
    WORK_LOCATION_POINTS = "work_location_points"
    IS_CRITICAL_WORK = "is_critical_work"
    CRITICAL_WORK_TYPES = "critical_work_type"
    ROUTINE_OR_NON_ROUTINE = "routine_or_non_routine"
    CASE_STATUS = "case_status"
    SUBMITTED_DATE = "submitted_date"
    SUBMITTED_TIME = "submitted_time"
    SUBCONTRACTOR = "subcontractor"
    HIRA = "HIRA"
    HIRA_LOWER = "hira"
    COUNT_HIRA = "count_hira"
    REMARK = "remark"
    COUNT = "count"
    DATE_OF_OBSERVATION = "date_of_observation"
    STATUS = "status"
    TYPE_OF_WORK_ACTIVITY = "work_activity"
    SIGNIFICANT_LEVEL = "significant_of_obs"
    IS_COMPLETE_OVER_80 = "is_complete_over_80"
    PROCESS_G = "process_g"
    SCORE_A = "score_a"
    SCORE_B = "score_b"
    SCORE_C = "score_c"
    SCORE_D = "score_d"
    SCORE_E = "score_e"
    SCORE_F = "score_f"
    SCORE_G = "score_g"
    SCORE_H = "score_h"
    SCORE_I = "score_i"
    SCORE_J1 = "score_j1"
    SCORE_J2 = "score_j2"
    INHERENT_SCORE = "inherent_score"
    INHERENT_GROUP = "inherent_risk"
    CONTROL_MEASURE_SCORE = "control_measure_score"
    CONTROL_MEASURE_GROUP = "control_measures"
    RESIDUAL_RISK_GROUP = "residual_risk_group"
    RESIDUAL_RISK_SCORE = "residual_risk_score"
    MATRIX_MODEL = "model"
    MATRIX_TYPE_ROW = "type"
    MATRIX_LOW_DATA = "low"
    MATRIX_MEDIUM_DATA = "medium"
    MATRIX_HIGH_DATA = "high"
    DATE = "date"
    DATETIME = "datetime"
    TIME_RANGE = "time_range"
    PROFILE_RESULT = "profiled_status"
    CRITICAL_WORK = "critical_work"
    NO_OF_HIRA = "no_of_hira"
    WORK_ON_EXISTING_SYSTEM = "work_on_existing_system"
    NON_ROUTINE_WORK = "non_routine_work"
    WORK_AT_STOCKPILE = "work_at_stockpile"
    TOP5_SAFETY_RISK = "top5_safety_risk"
    WORK_COMPLETION = "work_completion"
    VSS_DEPLOYMENT = "vss_deployment"
    NUM_OF_INSPECTIONS = "num_of_inspections"
    OBSERVATIONS = "observations"
    SIGNIFICANT_OBSERVATIONS = "significant_observations"


class WorkerProfilingColumn(Enum):
    IDENTITY_NUMBER = "identity_number"
    SUBCONTRACTORS = "subcontractors"
    PACKAGES = "packages"
    STATUS = "status"
    CREATED_AT = "created_at"
    CONTRACTOR_TYPE = "contractor_type"
    USER_TYPE = "user_type"
    MAIN_CONTRACTOR = "main_contractor"
    REMARK = "remark"
    PACKAGE = "package"
    SUBCONTRACTOR = "subcontractor"
    PROFILED_STATUS = "profiled_status"
    DATE = "date"


class SubconRiskScoreValues(Enum):
    SCORE_A_MAX = 17.8
    SCORE_A_MIN = 0
    SCORE_B_MAX = 19.7
    SCORE_B_MIN = 0
    SCORE_B_CONDITION_1_RESULT = 19.7
    SCORE_B_CONDITION_2_RESULT = 15
    SCORE_B_CONDITION_3_RESULT = 5

    SCORE_C_CONDITION_1_MIN = 0.1
    SCORE_C_CONDITION_1_MAX = 0.99
    SCORE_C_CONDITION_1_RESULT = 5
    SCORE_C_CONDITION_2_MIN = 1
    SCORE_C_CONDITION_2_MAX = 1.49
    SCORE_C_CONDITION_2_RESULT = 10
    SCORE_C_CONDITION_3_MIN = 1.5
    SCORE_C_CONDITION_3_MAX = 1.99
    SCORE_C_CONDITION_3_RESULT = 12.5
    SCORE_C_CONDITION_4_MIN = 2
    SCORE_C_CONDITION_4_MAX = 2.49
    SCORE_C_CONDITION_4_RESULT = 15
    SCORE_C_CONDITION_5_MIN = 2.5
    SCORE_C_CONDITION_5_MAX = 2.99
    SCORE_C_CONDITION_5_RESULT = 17.5
    SCORE_C_MAX = 19
    SCORE_C_MIN = 0
    SCORE_D_CONDITION_1_MIN = 0.01
    SCORE_D_CONDITION_1_MAX = 3
    SCORE_D_CONDITION_1_RESULT = 5
    SCORE_D_CONDITION_2_MIN = 3.01
    SCORE_D_CONDITION_2_MAX = 4
    SCORE_D_CONDITION_2_RESULT = 10
    SCORE_D_CONDITION_3_MIN = 4.01
    SCORE_D_CONDITION_3_MAX = 5
    SCORE_D_CONDITION_3_RESULT = 15
    SCORE_D_CONDITION_4_MIN = 5.01
    SCORE_D_CONDITION_4_MAX = 6
    SCORE_D_CONDITION_4_RESULT = 17.5
    SCORE_D_CONDITION_5_MIN = 6.01
    SCORE_D_CONDITION_5_RESULT = 21.4
    SCORE_D_MIN = 0
    SCORE_E_CONDITION_1_MIN = 0.1
    SCORE_E_CONDITION_1_MAX = 0.99
    SCORE_E_CONDITION_1_RESULT = 5
    SCORE_E_CONDITION_2_MIN = 1
    SCORE_E_CONDITION_2_MAX = 1.49
    SCORE_E_CONDITION_2_RESULT = 10
    SCORE_E_CONDITION_3_MIN = 1.5
    SCORE_E_CONDITION_3_MAX = 1.99
    SCORE_E_CONDITION_3_RESULT = 15
    SCORE_E_CONDITION_4_MIN = 2
    SCORE_E_CONDITION_4_MAX = 2.49
    SCORE_E_CONDITION_4_RESULT = 20
    SCORE_E_MAX = 22.1
    SCORE_E_MIN = 0

    SCORE_F_CONDITION_1 = 0
    SCORE_F_CONDITION_1_RESULT = 14.7
    SCORE_F_CONDITION_2 = 1
    SCORE_F_CONDITION_2_RESULT = 10
    SCORE_F_CONDITION_3 = 2
    SCORE_F_CONDITION_3_RESULT = 5
    SCORE_F_CONDITION_4 = 3
    SCORE_F_CONDITION_4_RESULT = 2.5
    SCORE_F_CONDITION_5 = 4
    SCORE_F_CONDITION_5_RESULT = 0

    SCORE_G1_CONDITION_1 = 0
    SCORE_G1_CONDITION_1_RESULT = 0
    SCORE_G1_CONDITION_2 = 1
    SCORE_G1_CONDITION_2_RESULT = 10
    SCORE_G1_CONDITION_3 = 2
    SCORE_G1_CONDITION_3_RESULT = 20
    SCORE_G1_CONDITION_4 = 3
    SCORE_G1_CONDITION_4_RESULT = 30
    SCORE_G1_CONDITION_5 = 4
    SCORE_G1_CONDITION_5_RESULT = 40
    SCORE_G1_CONDITION_6 = 5
    SCORE_G1_CONDITION_6_RESULT = 50
    SCORE_G1_CONDITION_7 = 6
    SCORE_G1_CONDITION_7_RESULT = 60
    SCORE_G1_CONDITION_8 = 7
    SCORE_G1_CONDITION_8_RESULT = 70
    SCORE_G1_CONDITION_9 = 8
    SCORE_G1_CONDITION_9_RESULT = 80
    SCORE_G1_CONDITION_10 = 9
    SCORE_G1_CONDITION_10_RESULT = 90
    SCORE_G1_CONDITION_11 = 10
    SCORE_G1_CONDITION_11_RESULT = 100

    SCORE_G2_CONDITION_1 = 0
    SCORE_G2_CONDITION_1_RESULT = 0
    SCORE_G2_CONDITION_2 = 1
    SCORE_G2_CONDITION_2_RESULT = 20
    SCORE_G2_CONDITION_3 = 2
    SCORE_G2_CONDITION_3_RESULT = 40
    SCORE_G2_CONDITION_4 = 3
    SCORE_G2_CONDITION_4_RESULT = 60
    SCORE_G2_CONDITION_5 = 4
    SCORE_G2_CONDITION_5_RESULT = 80
    SCORE_G2_CONDITION_6 = 5
    SCORE_G2_CONDITION_6_RESULT = 100

    SCORE_G_MAX = 16.2
    SCORE_G_CONDITION_MAX = 100
    SCORE_G_CONDITION_BASE = 0.162
    NUM_OF_OBS_LOW_CONDITION_LOWER = 0
    NUM_OF_OBS_LOW_CONDITION_UPPER = 30
    NUM_OF_OBS_MED_CONDITION_LOWER = 31
    NUM_OF_OBS_MED_CONDITION_UPPER = 60

    SCORE_H1_CONDITION_1 = 0
    SCORE_H1_CONDITION_1_RESULT = 0
    SCORE_H1_CONDITION_2 = 1
    SCORE_H1_CONDITION_2_RESULT = 50
    SCORE_H1_CONDITION_3 = 2
    SCORE_H1_CONDITION_3_RESULT = 100

    SCORE_H2_CONDITION_1 = 0
    SCORE_H2_CONDITION_1_RESULT = 0
    SCORE_H2_CONDITION_2 = 1
    SCORE_H2_CONDITION_2_RESULT = 10
    SCORE_H2_CONDITION_3 = 2
    SCORE_H2_CONDITION_3_RESULT = 30
    SCORE_H2_CONDITION_4 = 3
    SCORE_H2_CONDITION_4_RESULT = 70
    SCORE_H2_CONDITION_5 = 4
    SCORE_H2_CONDITION_5_RESULT = 100

    SCORE_H3_CONDITION_1 = 0
    SCORE_H3_CONDITION_1_RESULT = 0
    SCORE_H3_CONDITION_2 = 1
    SCORE_H3_CONDITION_2_RESULT = 5
    SCORE_H3_CONDITION_3 = 2
    SCORE_H3_CONDITION_3_RESULT = 15
    SCORE_H3_CONDITION_4 = 3
    SCORE_H3_CONDITION_4_RESULT = 35
    SCORE_H3_CONDITION_5 = 4
    SCORE_H3_CONDITION_5_RESULT = 50
    SCORE_H3_CONDITION_6 = 5
    SCORE_H3_CONDITION_6_RESULT = 75
    SCORE_H3_CONDITION_7 = 6
    SCORE_H3_CONDITION_7_RESULT = 100

    SCORE_H_CONDITION_MAX = 100
    SCORE_H_CONDITION_BASE = 0.162
    NUM_OF_INCIDENTS_LOW_CONDITION_LOWER = 0
    NUM_OF_INCIDENTS_LOW_CONDITION_UPPER = 5
    NUM_OF_INCIDENTS_MED_CONDITION_LOWER = 6
    NUM_OF_INCIDENTS_MED_CONDITION_UPPER = 15

    SCORE_I_MAX = 100
    SCORE_I_CONDITION_BASE = 0.136
    SAFETY_PERFORMANCE_LOW_CONDITION_LOWER = 0
    SAFETY_PERFORMANCE_LOW_CONDITION_UPPER = 5.45

    SCORE_J_MAX = 100
    SCORE_J_CONDITION_BASE = 0.16
    MAIN_CONTRACTOR_SSPA_BOUNDARY_CONDITION = 6.4

    SCORE_K_MAX = 12.8
    SCORE_K_MIN = 0
    SCORE_K_CONDITION = 90

    SCORE_L_CONDITION_BASE = 2
    SCORE_L_MAX = 10.5
    SCORE_L_MIN = 0

    CONTROL_MEASURE_1 = 24
    CONTROL_MEASURE_2 = 29
    INHERENT_1 = 39
    INHERENT_2 = 49


class WorkActivityScoreValue(Enum):
    """Column name

    Args:
        Enum (str): type of input file
    """
    # Enum for A
    A_SCORE_CRITICAL = 10
    A_SCORE_NON_CRITICAL = 0

    # Enum for B
    B_SCORE_RESULT_1 = 0
    B_SCORE_RESULT_2 = 2.5
    B_SCORE_RESULT_3 = 5
    B_SCORE_RESULT_4 = 10

    B_MAX_CONDITION_1 = 0

    B_MIN_CONDITION_2 = 1
    B_MAX_CONDITION_2 = 3
    B_MIN_CONDITION_3 = 4
    B_MAX_CONDITION_3 = 6
    B_MIN_CONDITION_4 = 7

    # Enum for C
    C_SCORE_SENSITIVE_WORK = 7.5
    C_SCORE_NON_SENSITIVE_WORK = 0

    # Enum for D
    D_SCORE_ROUTINE_WORK = 0
    D_SCORE_NON_ROUTINE_WORK = 5

    # Enum for E
    E_SCORE_STOCKPILE_WORK = 2.5
    E_SCORE_NON_STOCKPILE_WORK = 0

    # Enum for F
    F_SCORE_TOP_5_SAFETY_RISK = 7.5
    F_SCORE_NON_TOP_5_SAFETY_RISK = 0

    # Enum for G
    G_SCORE_RESULT_1 = 0
    G_SCORE_RESULT_2 = 2.5
    G_SCORE_RESULT_3 = 5
    G_SCORE_RESULT_4 = 7.5
    G_MAX_CONDITION_1 = 0.25
    G_MIN_CONDITION_2 = 0.26
    G_MAX_CONDITION_2 = 0.5
    G_MIN_CONDITION_3 = 0.51
    G_MAX_CONDITION_3 = 0.75

    # Enum for H
    H_SCORE_VSS_DEPLOYMENT = 5
    H_SCORE_NON_VSS_DEPLOYMENT = 0

    # Enum for I
    I_SCORE_RESULT_1 = 0
    I_SCORE_RESULT_2 = 5
    I_SCORE_RESULT_3 = 15
    I_SCORE_RESULT_4 = 25

    # Default
    DEFAULT_NULL_VALUE = 0.0

    # Enum for J1
    J1_SCORE_RESULT_1 = 0
    J1_SCORE_RESULT_2 = 5
    J1_SCORE_RESULT_3 = 10

    # Enum for J2
    J2_SCORE_SIGNIFICANT_OBSERVATIONS = 10
    J2_SCORE_NON_SIGNIFICANT_OBSERVATIONS = 0

    # Enum for result inherent risk
    LOW_MAX_CONDITION = 5
    MEDIUM_MIN_CONDITION = 5
    MEDIUM_MAX_CONDITION = 15

    # Enum for result control maasure
    STRONG_MAX_CONDITION = 19
    ACCEPTABLE_MIN_CONDITION = 19
    ACCEPTABLE_MAX_CONDITION = 33


class ProfiledStatus(Enum):
    PROFILED = "Profiled"
    NOT_PROFILED = "Not profiled"
    EXCLUSED = "Excluded"


class OsEnviron(Enum):
    REGION_NAME = 'REGION_NAME'
    SECRET_NAME = 'SECRET_NAME'
    BUCKET_NAME = 'BUCKET_NAME'
    RUNNING_ENV = "RUNNING_ENV"


class RequestParam(Enum):
    TYPE = 'type'
    FILTER_ID = 'filter_id'
    FILTER_START_DATE = 'filter_start_date'
    FILTER_END_DATE = 'filter_end_date'
    PAGE_SIZE = 'page_size'
    PAGE = 'page'
    FILTER_WORK_COMPANY = 'filter_work_company'
    FILTER_WORK_DATE = 'filter_work_date'
    FILTER_PACKAGE = 'filter_package'
    FILTER_WORK_TYPE = 'filter_work_type'
    OUTPUT_FILENAME = "output_filename"
    PAGE_NUMBER = "PageNumber"
    PAGE_SIZE_PASCAL_CASE = "PageSize"


class RequestHeader(Enum):
    X_API_KEY = 'x-api-key'
    CONTENT_TYPE = 'Content-Type'
    CONTENT_TYPE_APPLICATION_JSON = 'application/json'
    X_CLIENT_ID = 'X-Client-Id'
    ACCEPT = 'accept'


class ReponseHeader(Enum):
    X_TOTAL_PAGE = "X-Total-Page"
    X_TOTAL_COUNT = "X-Total-Count"
    X_CURRENT_PAGE = "X-Current-Page"


class StatusCode(Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    INTERNAL_SERVER_ERROR = 500


class ResponseColumn(Enum):
    STATUS = 'status'
    DATA = 'data'
    ITEMS = 'items'
    NEW_PAGE = 'newPage'
    PAGE = 'page'
    PAGE_SIZE = 'page_size'
    TOTAL_COUNT = 'total_count'
    PAGE_COUNT = 'page_count'
    ERROR_MESSAGE = 'error_message'


class ResponeStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"


class API(Enum):
    API_KEY = "api_key",
    API_URL = "api_url"


class IngestWdcColumns(Enum):
    WORKING_TIME = "working_time"
    START_WORK_TIME = "start_work_time"
    END_WORK_TIME = "end_work_time"


class CaseStatus(Enum):
    CLOSED = "closed"
    APPROVED = "approved"
    PENDING_APPROVAL = "pending approval"


class DateFormat(Enum):
    YYYY_MM_DD = 'yyyy-MM-dd'
    D_M_YYYY = "d/M/yyyy"
    M_D_YYYY = "M/d/yyyy"
    Y_M_D = "%Y-%m-%d"
    YYYY_MM_DD_MM_MM_SS_SSS = "yyyy-MM-dd HH:mm:ss.SSS"
    YYYY_MM_DD_HH_MM_SS = "yyyy-MM-dd HH:mm:ss"
    YYYY_M_D = "yyyy-M-d"


class TrueFalseValue(Enum):
    TRUE = "true"
    FALSE = "false"


class ARWColumns(Enum):
    PACKAGES = "packages"
    COMPANIES = "subcontractors"
    PROFILED_STATUS = "profiled_status"
    IDENTITY_NUMBER = "identity_number"
    DUE_DATE = "due_date"
    RESULT_SCORE = "result_score"
    STATUS = "status"
    DATE = "date"
    MONTH = "month"


class IngestTrainingColumns(Enum):
    USER_TYPES = "user_types"
    TRAINING_NAME = "training_name"
    RESULT_SCORE = "result_score"
    TOTAL_QUESTIONS = "total_questions"
    TRAINING_RESPONSE_ID = "training_response_id"
    DUE_DATE = "due_date"
    PACKAGES = "packages"
    COMPANIES = "companies"
    IDENTITY_NUMBER = "identity_number"
    STATUS = "status"
    COMPLETED_AT = "completed_at"


class TrainingStatus(Enum):
    COMPLETED = "Completed"
    PENDING = "Pending"
    OVERDUE = "Overdue"


class StatisticColumn(Enum):
    PACKAGE = 'package'
    DATE = 'date'
    EFFECTIVE_FROM = "effective_from"
    IS_ACTIVE = "is_active"
    VERSION = "version"
    HASHCODE = "hashcode"
    CREATE_AT = "created_at"
    UPDATE_AT = "updated_at"
    CREATE_BY = "created_by"
    UPDATE_BY = "updated_by"
    NO_OF_MANHOURS_FOR_THE_MONTH = "no_of_manhours_for_the_month"
    NO_OF_WORKERS_FOR_THE_MONTH = "no_of_workers_for_the_month"
    CUMULATIVE_AVE_NO_OF_WORKERS = "cumulative_ave_no_of_workers"
    NO_OF_MAJOR_INJURY_CASES_FOR_THE_MONTH = "no_of_major_injury_cases_for_the_month"
    NO_OF_MINOR_INJURY_CASES_FOR_THE_MONTH = "no_of_minor_injury_cases_for_the_month"
    CUMULATIVE_MAJOR_INJURY_RATE = "cumulative_major_injury_rate"
    CUMULATIVE_MINOR_INJURY_RATE = "cumulative_minor_injury_rate"


class IncidentRecordColumn(Enum):
    PACKAGE = 'package'
    DATE = 'date'
    MANDAYS_LOST = "mandays_lost"
    EFFECTIVE_FROM = "effective_from"
    IS_ACTIVE = "is_active"
    VERSION = "version"
    HASHCODE = "hashcode"
    CREATE_AT = "created_at"
    UPDATE_AT = "updated_at"
    CREATE_BY = "created_by"
    UPDATE_BY = "updated_by"


class StatisticAggColumn(Enum):
    REMARK = "remark"
    PACKAGE = "package"
    SUBCONTRACTOR = "subcontractor"
    NEW_CONTRACTOR = "new_contractor"
    NO_OF_FATAL = "no_of_fatal"
    NO_OF_ARRO_OCC = "no_of_aero_occ"
    NO_OF_WORKERS = "no_of_workers"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"
    CLASSIFICATION_OF_INCIDENTS = "classification_of_incidents"
    CREATE_AT = "created_at"
    UPDATE_AT = "updated_at"
    CREATE_BY = "created_by"
    UPDATE_BY = "updated_by"
    EFFECTIVE_FROM = "effective_from"
    EFFECTIVE_TO = "effective_to"
    IS_ACTIVE = "is_active"
    HASHCODE = "hashcode"
    VERSION = "version"
