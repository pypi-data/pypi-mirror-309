# 从光谱文件名中提取参数
# 文件名称格式如 spe_fFile_name = 'NPOM150-PIKE0P45-LASER[YSL-w785-p100%-nd220-35.92uW]-PI[1200ms-60um-150i-785c]-TEST[1-2-3]-oiDF-NC23 34.csv';
#              spe_file_name = 'NPOM150-PIKE0P45-TEST[1-2-3]-oiDF-NC23-BG 34.csv';
import re

class Spectrometer:
    def __init__(self):
        self.spe = "Spectrometer Parameters"
        self.devName = None
        self.expTime = None
        self.speUnit = "nm"

class Laser:
    def __init__(self):
        self.laser = "Laser parameters"
        self.devName = None
        self.waveLength = None
        self.powerSet1 = None
        self.powerSet2 = None
        self.powerValue = None
        self.powerUnit = None

class ExperimentalInfo:
    def __init__(self):
        self.expinfo = "Experimental parameters"
        self.sampleName = None
        self.speType = None
        self.partID = None
        self.partNote = None

def get_spe_info(spe_file_name: str):
    """
    Parse a spectrometer file name and return structured objects containing parsed results.
    
    :param spe_file_name: The file name to parse.
    :return: A tuple of Spectrometer, Laser, and ExperimentalInfo objects.
    """
    # Step 1: Remove `.csv` suffix, `.txt` suffix, and trailing sequence
    spe_file_str = re.sub(r'\.csv$', '', spe_file_name)
    spe_file_str = re.sub(r'\.txt$', '', spe_file_str)  # Remove `.txt` suffix
    spe_file_str = re.sub(r'\s\d*$', '', spe_file_str)
    spe_file_str = re.sub(r'_\d*$', '', spe_file_str)  # Remove trailing `_01`, `_02`, etc.

    # Replace secondary data delimiters inside brackets with '+'
    matches = list(re.finditer(r'-\w*\[.*?\]', spe_file_str))
    for match in reversed(matches):
        start, end = match.start(), match.end()
        modified = re.sub(r'-', '+', spe_file_str[start + 1:end])
        spe_file_str = spe_file_str[:start + 1] + modified + spe_file_str[end:]

    spe_file_str = spe_file_str.replace('[', '[+').replace(']', '+]')

    # Create objects
    spe = Spectrometer()
    laser = Laser()
    exp_info = ExperimentalInfo()

    # Step 2: Extract spectrometer information
    spectrometer_match = re.search(r'-(PI|HORIBA|BQVIS|BQNIR)\[.*?\]', spe_file_str)
    if spectrometer_match:
        spectrometer_str = spectrometer_match.group(0)[1:]
        parts = spectrometer_str.split('[')
        spe.devName = parts[0]
        params = parts[1]

        # Extract exposure time
        time_match = re.search(r'\+([\d.]+)ms', params)
        if time_match:
            spe.expTime = float(time_match.group(1)) / 1000  # Convert ms to seconds
        else:
            time_match = re.search(r'\+([\d.]+)s', params)
            if time_match:
                spe.expTime = float(time_match.group(1))

        # Extract spectrometer unit
        if "+um+" in params:
            spe.speUnit = "um"
        elif "+cm^-1+" in params:
            spe.speUnit = "cm^-1"
        else:
            spe.speUnit = "nm"

    # Step 3: Extract laser parameters
    laser_match = re.search(r'-LASER\[.*?\]', spe_file_str)
    if laser_match:
        laser_str = laser_match.group(0)[1:]
        parts = laser_str.split('[')
        params = parts[1]

        # Extract laser device name
        laser_name_match = re.search(r'\+(\w+)\+', params)
        if laser_name_match:
            laser.devName = laser_name_match.group(1)

        # Extract wavelength
        wavelength_match = re.search(r'\+(w|W)(\d{3,4})\+', params)
        if wavelength_match:
            laser.waveLength = int(wavelength_match.group(2))

        # Extract ND filter setting
        nd_match = re.search(r'\+(nd|ND)(\d{1,3})\+', params)
        if nd_match:
            laser.powerSet1 = nd_match.group(2)

        # Extract power percentage setting
        power_percent_match = re.search(r'\+(p|P)(\d{1,3})%\+', params)
        if power_percent_match:
            laser.powerSet2 = int(power_percent_match.group(2))

        # Extract laser power value and unit
        power_match = re.search(r'\+([\d.]+)(uW|mW|W)\+', params, re.IGNORECASE)
        if power_match:
            laser.powerValue = float(power_match.group(1))
            laser.powerUnit = power_match.group(2)

    # Step 4: Extract experimental information
    parts = spe_file_str.split('-')
    sample_name_match = re.match(r'[A-Z_0-9]+', parts[0])
    if sample_name_match and sample_name_match.group() == parts[0]:
        exp_info.sampleName = parts[0]

    # Extract experiment type
    experiment_match = re.search(r'(DF|oiDF|Raman|PL)', spe_file_str)
    if experiment_match:
        exp_info.speType = experiment_match.group(0)

    # Extract particle ID and BG note
    if parts[-1] == "BG":
        exp_info.partID = parts[-2]
        exp_info.partNote = "BG"
    else:
        exp_info.partID = parts[-1]
        exp_info.partNote = ""

    return spe, laser, exp_info
