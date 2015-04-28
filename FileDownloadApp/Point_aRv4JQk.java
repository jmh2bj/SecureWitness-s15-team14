<!DOCTYPE html>
<html lang="en">
<head>
    <title>SecureWitness</title>
</head>

<body>
    <div id="sidebar">
        
        <ul>
            <li><a href="/registration/create">New Account</a></li>
            <li><a href="/registration/login">Login</a></li>
            <li><a href="/registration/logout">Logout</a></li>
            <li><a href="/registration/confirm">Profile</a></li>
            <li><a href="/groups">Groups</a></li>
            <li><a href="/reports">Reports</a></li>
            <li><a href="/folders">Folders</a></li>
            <li><a href="/searchform">Search</a></li>
            <li><a href="/popular">Top Reports</a></li>
        </ul>
        
    </div>

    <div id="content">
        

<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<form method="post" action="" enctype="multipart/form-data">
    <input type='hidden' name='csrfmiddlewaretoken' value='sMdqbgbKoCNuUs829BzMKAV9gzBEZwvD' />
    
    <label for="id_rep_title">Report Title:</label>
    <input id="id_rep_title" maxlength="200" name="rep_title" type="text" value="random" /> <p/>
    
    <label for="id_short_desc">Short Description:</label>
    <input id="id_short_desc" maxlength="200" name="short_desc" type="text" value="random" /> <p/>
    
    <label for="id_detailed_desc">Detailed Description:</label>
    <input id="id_detailed_desc" maxlength="2000" name="detailed_desc" type="text" value="ranomd" /> <p/>
    
    <label for="id_loc">Location:</label>
    <input id="id_loc" maxlength="200" name="loc" type="text" /> <p/>
    
    <label for="id_rep_date">Report date:</label>
    <input id="id_rep_date" name="rep_date" type="text" value="1995-02-24 00:00:00" /> <p/>
    
    <label for="id_keywords">Associated Keywords:</label>
    <input id="id_keywords" maxlength="500" name="keywords" type="text" /> <p/>
    
    <label for="id_rep_file">Rep file:</label>
    Currently: <a href="reports/Point_aRv4JQk.java">reports/Point_aRv4JQk.java</a> <input id="rep_file-clear_id" name="rep_file-clear" type="checkbox" /> <label for="rep_file-clear_id">Clear</label><br />Change: <input id="id_rep_file" name="rep_file" type="file" /> <p/>
    
    <label for="id_isPublic">Public Report?</label>
    <input checked="checked" id="id_isPublic" name="isPublic" type="checkbox" /> <p/>
    
    <label for="id_allowed_users">Allowed Users:</label>
    <select multiple="multiple" id="id_allowed_users" name="allowed_users">
<option value="1">admin</option>
<option value="2">radom</option>
</select> <p/>
    
    <label for="id_allowed_groups">Allowed Groups:</label>
    <select multiple="multiple" id="id_allowed_groups" name="allowed_groups">
</select> <p/>
    
    <input type="submit" name="update_report" value="Update Report" />
    <input type="submit" name="copy_report" value="Copy Report" />
</form>


<li><a href="2/delete">Delete Report</a></li>

<li><a href="2/upvote">Upvote</a></li>
<li><a href="2/downvote">Downvote</a></li>

</body>
</html>


    </div>
</body>
</html>
