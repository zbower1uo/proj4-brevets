"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.

#indexes for opening and closing times
CLOSE = 1
OPEN = 0
#max,min speeds and distances used to break up controls/legs of race grouped with max/min
CONTROL_MAX_MIN = [[34,15,200],[32,15,200],[30,15,200],[26,13.333,300],[28,11.428,400]]
#OVERALL= {200: 13.5, 300: 20, 400: 27, 600: 40, 1000: 75}
#overall time for distances
OVERALL = {200:[13,30],300:[20,0],400:[27,0],600:[40,0],1000:[75,0]}
#Valid brevet distances
VALID_DISTANCES = [200, 400, 600, 1000]

def valid_input(control_dist_km,brevet_dist_km):
  """
  Args:
     control_dist_km:  number, the control distance in kilometers
     brevet_dist_km: number, the nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600,
         or 1000 (the only official ACP brevet distances)
  Returns:
     True if input(distances) are okay
  """
  #max dist is +10%
  if control_dist_km > brevet_dist_km * 1.1:
    return False
  if control_dist_km < 0:
    return False
  if brevet_dist_km not in VALID_DISTANCES:
    return False
  else:
    return True

#function to calculate code, reduces repetition
def calculate_time(control_dist_km, brevet_dist_km, brevet_start_time,index):
  """
  Args:
     control_dist_km:  number, the control distance in kilometers
     brevet_dist_km: number, the nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600,
         or 1000 (the only official ACP brevet distances)
     brevet_start_time:  An ISO 8601 format date-time string indicating
         the official start time of the brevet
     index: gets speed from max/min tables 1 = close 0 = open
  Returns:
     An ISO 8601 format date string indicating the control open time.
     This will be in the same time zone as the brevet start time.
  """
  if not valid_input(control_dist_km,brevet_dist_km):
    return None
  time = 0
  #calculate 0
  if (control_dist_km == 0):
    return arrow.get(brevet_start_time).shift(hours=+index).isoformat()
  
  #calculate time 
  if (control_dist_km >= brevet_dist_km):
    control_dist_km = brevet_dist_km
    #check max lim
    if (index == CLOSE):
      hour = OVERALL[control_dist_km][0]
      minn = OVERALL[control_dist_km][1]
      return arrow.get(brevet_start_time).shift(hours=+hour,minutes=+minn).isoformat()
  #Otherwise breakup and find times
  for s in CONTROL_MAX_MIN:
    #handle values not in the specific range, fixes going backward
    if control_dist_km <= 0:
      continue
    if control_dist_km > s[2]:
      time += s[2] / s[index]
    else:
      time += (control_dist_km / s[index])
    control_dist_km -= s[2]

  hour = int(time)
  minn = round(time * 60) % 60
  return arrow.get(brevet_start_time).shift(hours=+hour,minutes=+minn).isoformat()


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    return calculate_time(control_dist_km,brevet_dist_km,brevet_start_time,OPEN)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
       in kilometers, which must be one of 200, 300, 400, 600, or 1000
       (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    return calculate_time(control_dist_km,brevet_dist_km,brevet_start_time,CLOSE)
