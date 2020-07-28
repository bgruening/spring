// parameters
class Config
{
	// data
	Vec < string > ldata;
public:
	// constructor		
	Config()
	{
        // table
        Format::readList ("config.cnf", ldata);
        
        // read
        ptWeb = get ("ptWeb");
        ptCache = get ("ptCache");
        ptTemp = get ("ptTemp");
        ptData = get ("ptData");
        ptResults = get ("ptResults");
        dbHost = get ("dbHost");
        dbUser = get ("dbUser");
        dbPass = get ("dbPass");
        dbName = get ("dbName");
        dbPort	= Convert::toInt(get ("dbPort"));
        
        // generate temp		
        mkdir(ptTemp.c_str(), 0777);
	}

    // uuid
    string get_uuid()
    {
        timeval tm;
        gettimeofday(&tm, NULL);
        return Convert::toString(tm.tv_sec) + Convert::toString(tm.tv_usec);
    }

	// search
	string get (string name)
	{
        // read variables
        int nsize = ldata.size();
        for (int i = 0; i < nsize; i++)
            if (ldata[i].size() > 0)
        	if (ldata[i][0] != '#')
            if (ldata[i] == "[" + name + "]")
            if (nsize > i + 1)
                return ldata[i+1];
        
        // log
        Msg::write("Parameter %s not defined.", name.c_str());
        return "";
	}
    
    // files and directories
    string ptWeb, ptCache, ptData, ptResults, ptTemp;

    // database
    int    dbPort;
    string dbHost, dbName, dbPass, dbUser;
};
