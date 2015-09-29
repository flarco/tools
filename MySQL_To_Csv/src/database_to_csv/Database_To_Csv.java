/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package database_to_csv;

import My_Database.MySQL_Database;
import static System.Other.join;
import java.sql.SQLException;
import com.mysql.jdbc.JDBC4ResultSet;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;

/**
 *
 * @author larco
 */
public class Database_To_Csv {

    /**
     * 
     * java -jar "Database_To_Csv.jar" "/Data/db1" "," "debian" "3306" "db1" "admin" "password" "bank,places"
     * 
     * @param args the command line arguments
     * @throws java.sql.SQLException
     * @throws java.io.FileNotFoundException
     */
    public static void main(String[] args) throws SQLException, IOException {
        run(args);
    }
    public static void run(String[] args) throws SQLException, FileNotFoundException, IOException {
        // TODO code application logic here
        
        String delimiter = ",";
        String server = "debian";
        String port = "3306";
        String db_name = "db1";
        String user = "admin";
        String password = "";
        String table_name_filter = "bank,resumes";
        String write_header = "y";
        ArrayList<String> table_filter_list = new ArrayList<>();;
        String target_folder = "/Data/db1";
        String sql;
        
        System.out.println("Connecting to " + server + "...");
        MySQL_Database db_source = new MySQL_Database(server, port, db_name, user, password);
        
        if (args.length < 8) {
            System.out.println("Need 7 parameters! target_folder delimiter server port db_name user pass write_header table_name_filter(optional sep. by comma)");
            System.out.println("Exiting.");
            return;
        } else {
            target_folder = args[0];
            delimiter = args[1];
            server = args[2];
            port = args[3];
            db_name = args[4];
            user = args[5];
            password = args[6];
            write_header = args[7];
            
            if(args.length == 9){
                table_name_filter = args[8];
                
            }
        }
        
        if(table_name_filter.contains(","))
            table_filter_list.addAll(Arrays.asList(table_name_filter.split(",")));
        else
            table_filter_list.add(table_name_filter);
        
        sql = "SELECT * FROM INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = '" + db_name + "'";
        JDBC4ResultSet result_set = (JDBC4ResultSet) db_source.query(sql);
        ArrayList<String[]> data_array = db_source.get_array(result_set);
        
        int row_n = 1;
        for( String[] data_row: data_array ){
            if(row_n++ == 1)
                continue;
            
            String schema = data_row[1];
            String table = data_row[2];
            String type = data_row[3];
            String skip = "y";
            
            for(String filter : table_filter_list){
                if(table.contains(filter))
                    skip = "n";
            }
            
            if(skip.equals("y") && table_filter_list.size() > 0) // process all if no entry for table_name_filter
                continue;
            
            System.out.println("Processing " + type + " `" + schema + "`.`" + table + "`");
            
//            sql = "SELECT * FROM `" + schema + "`.`" + table + "` LIMIT 1";
            sql = "SELECT * FROM `" + schema + "`.`" + table + "`";
            result_set = (JDBC4ResultSet) db_source.query(sql);
            String fields[] = db_source.get_fields(result_set);
            
            if(type.equals("VIEW") && fields[0].equals("file_path")){ // Custom View
                ArrayList<String[]> data_view_path = db_source.get_array(result_set);
                String view_file_path = data_view_path.get(1)[0];
                System.out.println("   Opening " + view_file_path);
                String view_sql = new String(Files.readAllBytes(Paths.get(view_file_path)), StandardCharsets.UTF_8);
                result_set = (JDBC4ResultSet) db_source.query(view_sql);
                fields = db_source.get_fields(result_set);
            }
            
            String new_file_path = target_folder + "/" + schema + "." + table + ".csv";
            int line_number = 0;
            try (PrintWriter file = new PrintWriter(new_file_path)) {
                String text = "\"" +join(fields,"\"" + delimiter + "\"")+ "\"";
                if(write_header.equals("y"))
                    file.println(text);
                
                while (result_set.next()) {
                    line_number++;
                    String row_data[] = db_source.get_current_row(result_set);
                    text = "\"" +join(row_data,"\"" + delimiter + "\"")+ "\"";
                    file.println(text);
                    
                    if((line_number % 10000) == 0)
                        file.flush();
                        
                }
            }
            db_source.close();
            db_source = new MySQL_Database(server, port, db_name, user, password);
        }
    }
    
}
