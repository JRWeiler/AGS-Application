def translate(state):
	state = state.lower()
	abv = ''
	if state == 'alabama':
		abv = 'AL'
	elif state == 'alaska':
		abv = 'AK'
	elif state == 'arizona':
		abv = 'AZ'
	elif state == 'arkansas':
		abv = 'AR'
	elif state == 'california':
		abv = 'CA'
	elif state == 'colorado':
		abv = 'CO'
	elif state == 'connecticut':
		abv = 'CT'
	elif state == 'delaware':
		abv = 'DE'
	elif state == 'florida':
		abv = 'FL'
	elif state == 'georgia':
		abv = 'GA'
	elif state == 'hawaii':
		abv = 'HI'
	elif state == 'idaho':
		abv = 'ID'
	elif state == 'illinois':
		abv = 'IL'
	elif state == 'indiana':
		abv = 'IN'
	elif state == 'iowa':
		abv = 'IA'
	elif state == 'kansas':
		abv = 'KS'
	elif state == 'kentucky':
		abv = 'KY'
	elif state == 'louisiana':
		abv = 'LA'
	elif state == 'maine':
		abv = 'ME'
	elif state == 'maryland':
		abv = 'MD'
	elif state == 'massachusetts':
		abv = 'MA'
	elif state == 'michigan':
		abv = 'MI'
	elif state == 'minnesota':
		abv = 'MN'
	elif state == 'mississippi':
		abv = 'MS'
	elif state == 'missouri':
		abv = 'MO'
	elif state == 'montana':
		abv = 'MT'
	elif state == 'nebraska':
		abv = 'NE'
	elif state == 'nevada':
		abv = 'NV'
	elif state == 'new hampshire':
		abv = 'NH'
	elif state == 'new jersey':
		abv = 'NJ'
	elif state == 'new mexico':
		abv = 'NM'
	elif state == 'new york':
		abv = 'NY'
	elif state == 'north carolina':
		abv = 'NC'
	elif state == 'north dakota':
		abv = 'ND'
	elif state == 'ohio':
		abv = 'OH'
	elif state == 'oklahoma':
		abv = 'OK'
	elif state == 'oregon':
		abv = 'OR'
	elif state == 'pennsylvania':
		abv = 'PA'
	elif state == 'rhode island':
		abv = 'RI'
	elif state == 'south carolina':
		abv = 'SC'
	elif state == 'south dakota':
		abv = 'SD'
	elif state == 'tennessee':
		abv = 'TN'
	elif state == 'texas':
		abv = 'TX'
	elif state == 'utah':
		abv = 'UT'
	elif state == 'vermont':
		abv = 'VT'
	elif state == 'virginia':
		abv = 'VA'
	elif state == 'washington':
		abv = 'WA'
	elif state == 'west virginia':
		abv = 'WV'
	elif state == 'wisconsin':
		abv = 'WI'
	elif state == 'wyoming':
		abv = 'WY'
	elif state == 'american samoa':
		abv = 'AS'
	elif state == 'district of columbia':
		abv = 'DC'
	elif state == 'federated states of micronesia':
		abv = 'FM'
	elif state == 'guam':
		abv = 'GU'
	elif state == 'marshall islands':
		abv = 'MH'
	elif state == 'northern mariana islands':
		abv = 'MH'
	elif state == 'palau':
		abv = 'PW'
	elif state == 'puerto rico':
		abv = 'PR'
	elif state == 'virgin islands':
		abv = 'VI'
	else:
		abv = state

	return abv