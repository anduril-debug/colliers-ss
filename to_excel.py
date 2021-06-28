from sitkva.models import Flat,House
import pandas as pd
import numpy as np
import requests



def flat_to_excel():

    flats = Flat.query.all()



    columns = ["Status","Region","Municipality","Sector","District","SubDistrict","Date","Full_cadastral_code","Land_cadastral","Address",
                "Area","Rooms","Floor","Total floors","Price total (USD)","Price (USD) per sqm","Property Type","Project Type",
                "Project Subtype","Remodelling","X","Y","Pipeline Project",	"Pipeline Subproject","Parent Developer","Completion Period","Is_MP_Overall"]





def state_to_excel():

    flats = Flat.query.all()

    columns = ["state"]

    
