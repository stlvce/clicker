BOOST_TYPE_NAME_TO_NUMBER = {
    'casual': 0, 
    'auto': 1, 
}

BOOST_TYPE_CHOICES = {
    (BOOST_TYPE_NAME_TO_NUMBER['casual'], 'casual'),
    (BOOST_TYPE_NAME_TO_NUMBER['auto'], 'auto'),
}

BOOST_TYPE_VALUES = {
    BOOST_TYPE_NAME_TO_NUMBER['casual']: {
        'click_power_scale': 1, 
        'auto_click_power_scale': 0, 
        'price_scale': 5,
    },
    BOOST_TYPE_NAME_TO_NUMBER['auto']: {
        'click_power_scale': 0,
        'auto_click_power_scale': 1, 
        'price_scale': 25, 
    }
}