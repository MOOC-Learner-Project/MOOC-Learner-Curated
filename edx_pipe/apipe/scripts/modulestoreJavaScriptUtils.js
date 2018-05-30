                   /* ************* Class CourseInfoExtractor *************** */

//Class definition/constructor:
function CourseInfoExtractor() {

    this.stanfordEnrollDomain = "shib:https://idp.stanford.edu/";

    this.allQuartersArr = ["fall", "winter", "spring", "summer"];
    // To change start month/day of quarter starts, 
    // change the following four partial month-dayTtime strings:
    this.fallStartStr   = "-09-01T00:00:00Z";
    this.winterStartStr = "-12-01T00:00:00Z";
    this.springStartStr = "-03-01T00:00:00Z";
    this.summerStartStr = "-06-01T00:00:00Z";

    // Create start months from above partial date strings:
    thisYear = new Date().getFullYear();
    // See class RealDate below about need for this class:
    this.fallQuarterStartMonth   = new RealDate(this.getQuarterStartDate(thisYear, "fall")).getMonth();
    this.winterQuarterStartMonth = new RealDate(this.getQuarterStartDate(thisYear, "winter")).getMonth();
    this.springQuarterStartMonth = new RealDate(this.getQuarterStartDate(thisYear, "spring")).getMonth();
    this.summerQuarterStartMonth = new RealDate(this.getQuarterStartDate(thisYear, "summer")).getMonth();

}


                   /* ************* Methods for CourseInfoExtractor *************** */

     //------------------------------
     // getQuarterStartDate 
     //---------------- 

     CourseInfoExtractor.prototype.getQuarterStartDate = function(theYear, quarter) {
         switch (quarter) {
         case "fall":
     	return(theYear     + this.fallStartStr);
     	break;
         case "winter":
     	return((Number(theYear)+1) + this.winterStartStr);
     	break;
         case "spring":
     	return((Number(theYear)+1) + this.springStartStr);
     	break;
         case "summer":
     	return((Number(theYear)+1) + this.summerStartStr);
     	break;
         }
     }

     //------------------------------
     // getQuarterFromDate 
     //---------------- 

     CourseInfoExtractor.prototype.getQuarterFromDate = function(dateStr) {

         var dateObj;
         try {
     	dateObj   = new RealDate(dateStr);
         } catch(err) {
     	return("unknown");
         }

         var dateMonth = dateObj.getMonth()
         if (dateMonth >= this.fallQuarterStartMonth && dateMonth > this.winterQuarterStartMonth) {
     	return "fall";
         } else if (dateMonth >= this.winterQuarterStartMonth && dateMonth < this.springQuarterStartMonth) {
     	return "winter";
         } else if (dateMonth >= this.springQuarterStartMonth && dateMonth < this.summerQuarterStartMonth) {
     	return "spring";
         } else return "summer";
     }

     //------------------------------
     // getNumQuartersDuration 
     //---------------- 

     // Given two date strings, return the number of quarters that
     // lie between those dates. If either of the given date is a
     // null date, or not a legal datetime string, return -1.

     CourseInfoExtractor.prototype.getNumQuartersDuration = function(startCalDate, endCalDate) {

         try {
     	     startDate = new RealDate(startCalDate);
	     if (startDate.isNullDateObj(startDate))
		 return(-1);
	 } catch(err) {
     	     return(-1);
         }
         startYear = startDate.getFullYear();
         thisYear  = startYear;
         startQuarter = this.getQuarterFromDate(startCalDate);

         thisQuarter  = startQuarter;

         try {
     	     endDate      = new RealDate(endCalDate);
	     if (endDate.isNullDateObj(endDate))
		 return(-1);
         } catch(err) {
     	     return(-1);
         }
         endQuarter   = this.getQuarterFromDate(endCalDate);
         endYear      = endDate.getFullYear();

         ///*********
         // print("Start quarter: " + startQuarter);
         // print("End quarter  : " + endQuarter);
         // print("Start year   : " + startYear);
         // print("End year     : " + endYear);
         // print("This quarter : " + thisQuarter);
         ///*********

         numQuarters = 1;
         while(true) {
     	nextQuarter = this.getNextQuarter(thisQuarter);

     	if (thisYear >= endYear && thisQuarter == endQuarter) {
     	    return numQuarters;
     	}

     	if (thisQuarter == "fall") {
     	    thisYear += 1;
     	}
     	thisQuarter = nextQuarter;
     	numQuarters += 1;

     	///*********
     	// print("thisYear   :  " + thisYear);
     	// print("thisQuarter:  " + thisQuarter);
     	// print("endYear    :  " + endYear);
     	// print("endQuarter :  " + endQuarter);
     	///*********

         }
     }

     //------------------------------
     // getNextQuarter 
     //---------------- 

     // Given a quarter string ('winter', 'spring,'...), return
     // the name of the following academic quarter.

     CourseInfoExtractor.prototype.getNextQuarter = function(thisQuarter) {
         thisQuarterIndx = this.allQuartersArr.indexOf(thisQuarter);
         if (thisQuarterIndx == this.allQuartersArr.length - 1) {
     	return this.allQuartersArr[0];
         }
         return(this.allQuartersArr[thisQuarterIndx + 1]);
     }

     //------------------------------
     // createCourseCSV 
     //---------------- 

     CourseInfoExtractor.prototype.createCourseCSV = function(academicYear, quartersToDo) {
         // Main, workhorse method.
         // Create CSV with course info, and print to stdout.
         // If "year" is 0, include all years on record.
         // If "quarter" is "all", include all quarters.

         this.year = academicYear;
         this.quartersToDo  = quartersToDo;
         var quartersToCover = [];
         if (this.quartersToDo == 'all') {
     	quartersToCover = ["fall", "winter", "spring", "summer"];
         } else {
     	quartersToCover.push(this.quartersToDo);
         }

         var quarterStartDate;
         var nextQuarterStartDate;
         var moreYearsToDo = true;
         var thisAcademicYear = this.year;
         var currYear = new Date().getFullYear();
         var theQuarterIndx  = 0;
         var nextQuarterIndx = 1;

         // If doing all years, set year to start
         // year of recorded history. OK to set it
         // earlier than true first recorded courses:
         if (thisAcademicYear == 0) {
     	thisAcademicYear = 2010;
         }
         // Distinguish between academic and calendar year:
         thisCalYear = thisAcademicYear;

         ///**********
         //print(thisAcademicYear);
         //print(thisCalYear);
         //print(quartersToCover);
         ///**********
         print("course_display_name,course_catalog_name,academic_year,quarter,num_quarters,is_internal,enrollment_start,start_date,end_date");

         while (moreYearsToDo) {
     	var currQuarter = quartersToCover[theQuarterIndx];
     	quarterStartDate = this.getQuarterStartDate(thisAcademicYear, currQuarter);
     	nextQuarterStartDate = this.getQuarterStartDate(thisAcademicYear, this.getNextQuarter(currQuarter));

     	///**********
     	// print("Quarter start     : " + quarterStartDate);
     	// print("Next Quarter start: " + nextQuarterStartDate);
     	///**********

     	// Get get course info for courses in
     	// one academic year, one particular quarter:
     	courseCursor = db.modulestore.find({"_id.category": "course",
        					    "metadata.start": {$gte: quarterStartDate, $lt: nextQuarterStartDate}
     					   },
                           			   {"metadata.start": true, 
     					    "metadata.end": true, 
     					    "metadata.enrollment_domain":true, 
     					    "metadata.enrollment_start":true, 
     					    "metadata.display_name":true}
     					  );

     	while (true) {
     	    doc = courseCursor.hasNext() ? courseCursor.next() : null;
     	    if (doc === null) {
     		break;
     	    }
     	    // Compute how many quarters course runs:
     	    numQuarters = this.getNumQuartersDuration(doc.metadata.start, doc.metadata.end);

     	    // Some records don't have class start or end
     	    // dates. Use zero-dates for those:
     	    startDate = doc.metadata.start;
     	    startDate = new RealDate(startDate).getMySqlDateStr();

     	    endDate = doc.metadata.end;
     	    endDate = new RealDate(endDate).getMySqlDateStr();

     	    enrollmentStartDate = doc.metadata.enrollment_start;
     	    enrollmentStartDate = new RealDate(enrollmentStartDate).getMySqlDateStr();

     	    isInternal = doc.metadata.enrollment_domain;
     	    if (isInternal == this.stanfordEnrollDomain || doc._id.org == "ohsx" || doc._id.org == "ohs") {
     		isInternal = 1;
     	    } else {
     		isInternal = 0;
     	    }

     	    if (endDate === undefined) {
     		// '.prototype' to use getNullDateStr as a class method:
     		endDate = RealDate.prototype.getNullDateStr();
     	    }
     	    print(doc._id.org +
     		  "/" + doc._id.course +
     		  "/" + doc._id.name +
     		  ",\"" + doc.metadata.display_name + "\"" +
     		  "," + thisAcademicYear +
     		  "," + currQuarter +
     		  "," + numQuarters +
     		  "," + isInternal +
     		  "," + enrollmentStartDate +
     		  "," + startDate +
     		  "," + endDate);
     	}
     	// Done with one quarter

     	// What is the next quarter
     	// of the quarters we are supposed to cover?
     	theQuarterIndx += 1;
     	if (theQuarterIndx > quartersToCover.length - 1) {
     	    // Did all wanted quarters for current academic year:
     	    theQuarterIndx = 0;
     	    // Do just one year?
     	    if (this.year > 0) {
     		// We are to do just one academic year:
     		moreYearsToDo = false;
     		continue;
     	    } else {
     		// Want same quarters for multiple years.
     		thisAcademicYear += 1;

     		// Adjust calendar year:
     		if (quartersToCover[theQuarterIndx] == "fall") {
     		    thisCalYear = thisAcademicYear;
     		} else {
     		    thisCalYear = thisAcademicYear + 1;
     		}

     		// Did all recorded years?
     		if (thisAcademicYear > currYear) {
     		    moreYearsToDo = false;
     		    continue;
     		}
     		// Do next year with same series of 
     		// quarters we just did for this year:
     		continue;
     	    }
     	}
     	// Still have quarters to do in current academic year.
     	// Calendar date increments, if switching from
             // Fall quarter to winter:
     	if (currQuarter == "fall" || this.year == 0) {
     	    // Just did fall quarter, or want all years for one 
     	    // Spring quarter happens in second
     	    // calendar year of the academic year:
     	    thisCalYear += 1;
     	    // Did all recorded years up to today's year plus 1?
     	    if (thisCalYear > currYear + 1) {
     		moreYearsToDo = false;
     		continue;
     	    }
     	}
         }
     }    

                    /* ************* Class RealDate *************** */

// Date class that fixes a seeming bug in MongoDB's
// JavaScript implementation. Its new ISODate("2014-01-01T07:00:00Z")
// returns 11 instead of 1 (or even 0 for zero-based month scheme.).
// My understanding is that 'Z' is local time.
// Note: this class only handles local time. It's all we need here.

function RealDate(isoDateStr) {
    if (isoDateStr === undefined || isoDateStr === null) {
	this.theDate = this.getNullDateStr();
	this.dateComponents = [];
    } else {
	this.theDate = isoDateStr;
	this.dateComponents = isoDateStr.split('-');
    }
}

                   /* ************* Methods for RealDate *************** */


    //------------------------------
    // toDateObj
    //---------------- 

    // Return an ISO date string.

    RealDate.prototype.toDateObj = function() {
        return(new ISODate(this.theDate));
    }

    //------------------------------
    // getYear 
    //---------------- 

    RealDate.prototype.getYear = function() {
        if (this.dateComponents.length > 0) {
    	return(Number(this.dateComponents[0]));
        } else {
    	return(0);
        }
    }

    //------------------------------
    // getFullYear 
    //---------------- 

    RealDate.prototype.getFullYear = function() {
        // Synonym to getYear()
        if (this.dateComponents.length > 0) {
    	return(Number(this.dateComponents[0]));
        } else {
    	return(0);
        }
    }

    //------------------------------
    // getMonth 
    //---------------- 

    RealDate.prototype.getMonth = function() {
        if (this.dateComponents.length > 1) {
    	return(Number(this.dateComponents[1]));
        } else {
    	return(0);
        }
    }

    //------------------------------
    // getDay 
    //---------------- 

    RealDate.prototype.getDay = function() {
        if (this.dateComponents.length > 2) {
    	dayPlusTPlusTime = this.dateComponents[2];
    	dayPlusTime = dayPlusTPlusTime.split('T');
    	return(Number(dayPlusTime[0]));
        } else {
    	return(0);
        }
    }

    //------------------------------
    // getTimeWithTimezone 
    //---------------- 

    RealDate.prototype.getTimeWithTimezone = function() {
        if (this.dateComponents.length > 2) {
    	dayPlusTPlusTime = this.dateComponents[2];
    	dayPlusTime = dayPlusTPlusTime.split('T');
    	return(dayPlusTime[1]);
        } else {
    	return("00:00:00:Z");
        }}

    //------------------------------
    // getTimeNoTimezone 
    //---------------- 

    RealDate.prototype.getTimeNoTimezone = function() {
        if (this.dateComponents.length > 2) {
    	dayPlusTPlusTime = this.dateComponents[2];
    	dayPlusTime = dayPlusTPlusTime.split('T');
    	timeWithTimeZone = dayPlusTime[1];
    	timeZoneSeparate = timeWithTimeZone.split('Z');
    	return(timeZoneSeparate[0]);
        } else {
    	return("00:00:00");
        }
    }


    //------------------------------
    // getMySqlDateStr 
    //---------------- 

    RealDate.prototype.getMySqlDateStr = function() {
        // Return a MySQL datetime-legal string.
        year = this.getYear();
        if (year == 0)
    	year = "0000";

        month = this.getMonth();
        if (month == 0)
    	month = "00";
        else if (month < 10)
    	month = "0" + month;

        day = this.getDay();
        if (day == 0)
    	day = "00";
        else if (day < 10)
    	day = "0" + day;

        mySqlDateStr = [year, month, day].join("-");
        mySqlStr = mySqlDateStr + ' ' + this.getTimeNoTimezone();
        return mySqlStr;
    }

    //------------------------------
    // getNullDateStr 
    //---------------- 

    RealDate.prototype.getNullDateStr = function() {
        // Return a MongoDB legal zero ISO date.
        // Note: Not legal in MySQL, b/c of the
        // 'T' and the timezone.
        return("0000-00-00T00:00:00.000Z");
    }
        

    //------------------------------
    // isNullDateObj
    //---------------- 

    // Return true if given RealDate *instance* is a null date,
    // else return false

    RealDate.prototype.isNullDateObj = function(realDateObj) {
	return(realDateObj.theDate == '0000-00-00T00:00:00.000Z' ||
	       realDateObj.theDate == '0000-00-00T00:00:00.Z' ||
	       realDateObj.theDate == '0000-00-00T00:00:00' ||
	       realDateObj.theDate == '0000-00-00' ||
	       realDateObj.theDate == '00:00:00' ||
	       realDateObj.theDate == '00:00:00Z')
    }

    //------------------------------
    // isNullDateStr
    //---------------- 

    // Return true if given string is a null date,
    // else return false

    RealDate.prototype.isNullDateStr = function(readDateStr) {
	return(readDateStr == '0000-00-00T00:00:00.000Z' ||
	       readDateStr == '0000-00-00T00:00:00Z' ||
	       readDateStr == '0000-00-00T00:00:00' ||
	       realDateObj.theDate == '0000-00-00' ||
	       realDateObj.theDate == '00:00:00' ||
	       realDateObj.theDate == '00:00:00Z')
    }

                   /* ************* Unit Tests *************** */

function realDateUnittests() {

    print('Tests for class RealDate...');

    rd = new RealDate('2014-01-02T10:11:12Z');

    // Jan 2 instead of Jan1 because of conversion GMT->PST
    if (String(rd.toDateObj()) !== 'Thu Jan 02 2014 02:11:12 GMT-0800 (PST)')
	raise("Conversion to ISO date failed.");
    else
	print('toDateObj() OK.');

    if (rd.getYear() !== 2014)
	raise("getYear() failed.");
    else
	print('getYear() OK.');

    if (rd.getFullYear() !== 2014)
	raise("getFullYear() failed.");
    else
	print('getFullYear() OK.');

    if (rd.getMonth() !== 1)
	raise("getMonth() failed.");
    else
	print('getMonth() OK.');

    if (rd.getDay() !== 2)
	raise("getDay() failed.");
    else
	print('getDay() OK.');

    if (rd.getTimeWithTimezone() !== '10:11:12Z')
	raise("getTimeWithTimezone() failed.");
    else
	print('getTimeWithTimezone() OK.');

    if (rd.getTimeNoTimezone() !== '10:11:12')
	raise("getTimeNoTimezone() failed.");
    else
	print('getTimeNoTimezone() OK.');

    if (rd.getMySqlDateStr() !== '2014-01-02 10:11:12')
	raise("getMySqlDateStr() failed.");
    else
	print('getMySqlDateStr() OK.');

    if (rd.isNullDateObj(rd))
	raise("isNullDateObj() failed.");
    else
	print('isNullDatObj() OK.');

    if (! rd.isNullDateStr('0000-00-00T00:00:00Z'))
	raise("isNullDataStr() failed.");
    else
	print('isNullDateStr() OK.');

    print('Class RealDate OK.');
}


function courseInfoExtractorUnittests() {

    print('Tests for class CourseInfoExtractor...');

    ce = new CourseInfoExtractor(2013, 'winter');

    if (ce.getQuarterStartDate(2013, 'summer') !== '2014-06-01T00:00:00Z')
	raise('getQuarterStartDate() failed.')
    else
	print('getQuarterStartDate() OK.')

    if (ce.getQuarterFromDate('2014-03-02') !== 'spring')
	raise('getQuarterFromDate() failed.')
    else
	print('getQuarterFromDate() OK.')

    if (ce.getNumQuartersDuration('2013-01-02', '2013-01-02') != 1)
	raise('getNumQuartersDuration() failed.')
    else
	print('getNumQuartersDuration() OK.')

    if (ce.getNumQuartersDuration('2013-01-02', '2014-01-02') != 5)
	raise('getNumQuartersDuration() failed.')
    else
	print('getNumQuartersDuration() OK.')

    if (ce.getNumQuartersDuration('2013-01-02', '0000-00-00') != -1)
	raise('getNumQuartersDuration() failed.')
    else
	print('getNumQuartersDuration() OK.')

    if (ce.getNumQuartersDuration('10:30:11', '00:00:00') != -1)
	raise('getNumQuartersDuration() failed.')
    else
	print('getNumQuartersDuration() OK.')

    if (ce.getNextQuarter('winter') != 'spring')
	print('getNextQuarter() failed.');
    else
	print('getNextQuarter() OK.');

    if (ce.getNextQuarter('summer') != 'fall')
	print('getNextQuarter() failed.');
    else
	print('getNextQuarter() OK.');
}
