package maindb

import (
	"online/global"
)

func GetAllDataFromMysql() global.TableSchema {
	rows, err := global.Mysql.Query("select ID, NAME, ADDRESS, LAT, LNG, LOCNAME, IMG, INTRO, ICON, TYPE from customers")
	if err != nil {
		return nil
	}
	var persons = make(global.TableSchema, 0)
	for rows.Next() {
		var a global.User
		err := rows.Scan(&a.ID, &a.NAME, &a.ADDRESS, &a.LAT, &a.LNG, &a.LOCNAME, &a.IMG, &a.INTRO, &a.ICON, &a.TYPE)
		if err != nil {
			return nil
		}
		persons = append(persons, a)
	}
	return persons
}

func GetDataFromMysqlFilterId(id string) global.TableSchema {
	rows, err := global.Mysql.Query("select ID, NAME, ADDRESS, LAT, LNG, LOCNAME, IMG, INTRO, ICON, TYPE from customers where id=?", id)
	if err != nil {
		return nil
	}
	var persons = make(global.TableSchema, 0)
	for rows.Next() {
		var a global.User
		err := rows.Scan(&a.ID, &a.NAME, &a.ADDRESS, &a.LAT, &a.LNG, &a.LOCNAME, &a.IMG, &a.INTRO, &a.ICON, &a.TYPE)
		if err != nil {
			return nil
		}
		persons = append(persons, a)
	}
	return persons
}
