import datetime
from collections import namedtuple

Guest = namedtuple('Guest', 'gnum rnum arrive depart gname')

def reservation() -> None:
    '''Prompt the user (using input()) for the name of the command file,
    and it should print its results (to the normal place, the console).'''
    cmd_f_name = str(input("Enter the name of the command file: "))
    infile = open(cmd_f_name, 'r').readlines()
    outfile = open('Rresults.txt', 'w')
    count = 0
    r_nums = []
    t_reservations = []
    gnum = 0
    for t in infile:
        clean_f = list(map(str.strip, infile)) # gets rid of '\n' within each of the elements within the list

    for p in range(len(clean_f)):
        if clean_f[p].lower().startswith('prl'): # PRL STANDS FOR PRINT LINE
            clean_f[p] = clean_f[p][4:].strip()
            outfile.write(clean_f[p] + '\n')
            print(clean_f[p])

        if clean_f[p].lower().startswith('anb'): # ANB STANDS FOR ADDING A SERVICE (EX: BEDROOM)
            if clean_f[p][4:].strip() not in r_nums:
                r_nums.append(clean_f[p][4:].strip())
            else:
                print("Sorry, can't add room {} again; it's already on the list.".format(clean_f[p][4:].strip()))
                outfile.write("Sorry, can't add room {} again; it's already on the list.\n".format(clean_f[p][4:].strip()))

        if clean_f[p].lower().startswith('deb'): # DEB STANDS FOR DELETE A SERVICE (EX: BEDROOM)
            if clean_f[p][4:].strip() not in r_nums:
                print("Sorry, can't delete room {}; it is not in service now".format(clean_f[p][4:].strip()))
                outfile.write("Sorry, can't delete room {}; it is not in service now \n".format(clean_f[p][4:].strip()))
            else:
                toBeRemoved = []
                toBeRemovedVals = []
                for l in range(len(t_reservations)):
                    if clean_f[p][4:].strip() == t_reservations[l].rnum:
                        toBeRemoved.append(l)
                        toBeRemovedVals.append(t_reservations[l])
                if toBeRemoved != []:
                    for i in toBeRemoved:
                        outfile.write("Deleting room {} forces cancellation of this reservation:\n".format(clean_f[p][4:]))
                        print("Deleting room {} forces cancellation of this reservation:".format(clean_f[p][4:]))
                        outfile.write("   {} arriving {} and departing {} (Conf. #{})\n".format(t_reservations[i].gname, t_reservations[i].arrive, t_reservations[i].depart, t_reservations[i].gnum))
                        print("   {} arriving {} and departing {} (Conf. #{})".format(t_reservations[i].gname, t_reservations[i].arrive, t_reservations[i].depart, t_reservations[i].gnum))
                    for i in toBeRemovedVals:
                        t_reservations.remove(i)

            for l in range(len(r_nums)):
                if r_nums[l] == clean_f[p][4:].strip():
                    r_nums.remove(clean_f[p][4:].strip())
                    break

        if clean_f[p].lower().startswith('rar'): # RAR STANDS FOR RESERVE A SERVICE (EX: ROOM)
            cleanlist = clean_f[p][4:].strip().split(' ')
            cleanlist = [x for x in cleanlist if x != '']
            rnum, arrive, depart = cleanlist[:3]
            gname = ' '.join(cleanlist[3:])
            arriveM, arriveD, arriveY = arrive.split('/')
            departM, departD, departY = depart.split('/')
            arriveDateTime = datetime.date(int(arriveY), int(arriveM), int(arriveD))
            departDateTime = datetime.date(int(departY), int(departM), int(departD))
            arriveX = '/'.join([x.rjust(2) for x in arrive.split('/')])
            departX = '/'.join([x.rjust(2) for x in depart.split('/')])

            if arriveDateTime > departDateTime:
                outfile.write("Sorry, can't reserve room {} ({} to {});\n".format(rnum, arrive, depart))
                print("Sorry, can't reserve room {} ({} to {});".format(rnum, arrive, depart))
                outfile.write("    can't leave before you arrive.\n")
                print("    can't leave before you arrive.")
            elif arriveDateTime == departDateTime:
                outfile.write("Sorry, can't reserve room {} ({} to {});\n".format(rnum, arrive, depart))
                print("Sorry, can't reserve room {} ({} to {});".format(rnum, arrive, depart))
                outfile.write("    can't arrive and leave on the same day.")
                print("    can't arrive and leave on the same day.")
            else:
                cantReserve = False
                for r in range(len(t_reservations)):
                    currentArriveM, currentArriveD, currentArriveY = t_reservations[r].arrive.split('/')
                    currentDepartM, currentDepartD, currentDepartY = t_reservations[r].depart.split('/')
                    currentArriveDateTime = datetime.date(int(currentArriveY), int(currentArriveM), int(currentArriveD))
                    currentDepartDateTime = datetime.date(int(currentDepartY), int(currentDepartM), int(currentDepartD))
                    if rnum == t_reservations[r].rnum:
                        # arriveDateTime is the new guy trying to make a reservation
                        # currentArriveDateTime is who in the table we're currently comparing it to
                        if (arriveDateTime == currentArriveDateTime and departDateTime == currentDepartDateTime) or (arriveDateTime >= currentArriveDateTime and departDateTime <= currentDepartDateTime) or (currentArriveDateTime < departDateTime < currentDepartDateTime):
                            outfile.write("Sorry, can't reserve room {} ({} to {});\n".format(t_reservations[r].rnum, arriveX, departX))
                            print("Sorry, can't reserve room {} ({} to {});".format(t_reservations[r].rnum, arriveX, departX))
                            outfile.write("   it's already booked (Conf. #{})\n".format(t_reservations[r].gnum))
                            print("   it's already booked (Conf. #{})".format(t_reservations[r].gnum))
                            cantReserve = True
                            break
                if cantReserve == False:
                    if rnum in r_nums:
                        gnum += 1
                        newRes = Guest(str(gnum), rnum, arriveX, departX, gname)
                        if newRes not in t_reservations:
                            t_reservations.append(newRes)
                            outfile.write("Reserving room {} for {} -- Confirmation #{}\n".format(rnum, gname, str(gnum)))
                            print("Reserving room {} for {} -- Confirmation #{}".format(rnum, gname, str(gnum)))
                            outfile.write("    (arriving {}, departing {})\n".format(arrive, depart))
                            print("    (arriving {}, departing {})".format(arrive, depart))
                    else:
                        outfile.write("Sorry; can't reserve room {}; room not in service\n".format(rnum))
                        print("Sorry; can't reserve room {}; room not in service".format(rnum))

        count += clean_f[p].lower().count('anb')
        if clean_f[p].lower().startswith('lob'): # LOB STANDS FOR LISTING ALL THE SERVICES (EX: BEDROOMS) CURRENTLY AVAILABLE
            date = clean_f[p][4:].strip().split()
            if len(date) >= 2:
                outfile.write("Bedrooms occupied between {} to {}:\n".format(date[0], date[1]))
                print("Bedrooms occupied between {} to {}:".format(date[0], date[1]))
                date0M, date0D, date0Y = date[0].split("/")
                date1M, date1D, date1Y = date[1].split("/")
                date[0] = datetime.date(int(date0Y), int(date0M), int(date0D))
                date[1] = datetime.date(int(date1Y), int(date1M), int(date1D))
                reserved = set()
                free = set()
                notNeeded = set()
                for n in range(len(t_reservations)):
                    dateArriveM, dateArriveD, dateArriveY = t_reservations[n].arrive.split("/")
                    dateDepartM, dateDepartD, dateDepartY = t_reservations[n].depart.split("/")
                    dateArrive = datetime.date(int(dateArriveY), int(dateArriveM), int(dateArriveD))
                    dateDepart = datetime.date(int(dateDepartY), int(dateDepartM), int(dateDepartD))
                    if not (date[0] <= dateArrive <= date[1]) and not (dateArrive <= date[0] <= dateDepart): # not in between
                        free.add(t_reservations[n].rnum)
                    elif (date[0] == date[1] and not (dateArrive <= date[1] < dateDepart)): # the same date
                        free.add(t_reservations[n].rnum)
                    if dateArrive < date[0] < dateDepart and t_reservations[n].rnum in free:
                        notNeeded.add(t_reservations[n].rnum)
                    reserved.add(t_reservations[n].rnum)
                unreserved = set(r_nums) - reserved
                free |= unreserved
                free -= notNeeded
                for rnum in set(r_nums)-free:
                    outfile.write("   {}\n".format(rnum))
                    print("   {}".format(rnum))
            else:
                outfile.write('Number of bedrooms in service:  ' + str(count) + '\n')
                print('Number of bedrooms in service:  ' + str(count))
                outfile.write('------------------------------------' + '\n')
                print('------------------------------------')
                for m in range(len(r_nums)):
                    outfile.write(r_nums[m] + '\n')
                    print(r_nums[m])

        if clean_f[p].lower().startswith('dar'): # DAR STANDS FOR DELETE A RESERVATION
            confirmation_num = clean_f[p][4:].strip()
            toBeRemoved = None
            for r in range(len(t_reservations)):
                if confirmation_num == t_reservations[r].gnum:
                    toBeRemoved = r
                    break
            if toBeRemoved == None:
                outfile.write("Sorry, can't cancel reservation; no confirmation number\n", confirmation_num)
                print("Sorry, can't cancel reservation; no confirmation number", confirmation_num)
            else:
                t_reservations.remove(t_reservations[toBeRemoved])

        if clean_f[p].lower().startswith('lar'): # LAR STANDS FOR LIST ALL RESERVATIONS
            outfile.write("Number of reservations: " + str(len(t_reservations)) + '\n')
            print("Number of reservations: ", len(t_reservations))
            outfile.write("No. Rm. Arrive     Depart     Guest\n")
            print("No. Rm. Arrive     Depart     Guest")
            outfile.write("------------------------------------------------\n")
            print("------------------------------------------------")
            for y in range(len(t_reservations)):
                outfile.write("{} {} {} {} {}\n".format(str(t_reservations[y].gnum).rjust(3), str(t_reservations[y].rnum), str(t_reservations[y].arrive), str(t_reservations[y].depart), str(t_reservations[y].gname)))
                print("{} {} {} {} {}".format(str(t_reservations[y].gnum).rjust(3), str(t_reservations[y].rnum), str(t_reservations[y].arrive), str(t_reservations[y].depart), str(t_reservations[y].gname)))

        if clean_f[p].lower().startswith('rbb'): # RBB STANDS FOR RESERVATION BY SERVICE (EX: BEDROOM)
            outfile.write("Reservations for room {}:\n".format(clean_f[p][4:].strip()))
            print("Reservations for room {}:".format(clean_f[p][4:].strip()))
            for z in range(len(t_reservations)):
                if t_reservations[z].rnum == clean_f[p][4:].strip():
                    outfile.write("   {} to {}:  {}\n".format(t_reservations[z].arrive, t_reservations[z].depart, t_reservations[z].gname))
                    print("   {} to {}:  {}".format(t_reservations[z].arrive, t_reservations[z].depart, t_reservations[z].gname))

        if clean_f[p].lower().startswith('rbg'): # RBG STANDS FOR RESERVATION BY GUEST
            outfile.write("Reservations for {}:\n".format(clean_f[p][4:].strip()))
            print("Reservations for {}:".format(clean_f[p][4:].strip()))
            for f in range(len(t_reservations)):
                if t_reservations[f].gname == clean_f[p][4:].strip():
                    outfile.write("   {} to {}:  room {}\n".format(t_reservations[f].arrive, t_reservations[f].depart, t_reservations[f].rnum))
                    print("   {} to {}:  room {}".format(t_reservations[f].arrive, t_reservations[f].depart, t_reservations[f].rnum))

        if clean_f[p].lower().startswith('laa'): # LAA STANDS FOR LIST ALL ARRIVALS
            outfile.write("Guests arriving on {}:\n".format(clean_f[p][4:].strip()))
            print("Guests arriving on {}:".format(clean_f[p][4:].strip()))
            for d in range(len(t_reservations)):
                if t_reservations[d].arrive == clean_f[p][4:].strip():
                    outfile.write("   {} (room {})\n".format(t_reservations[d].gname, t_reservations[d].rnum))
                    print("   {} (room {})".format(t_reservations[d].gname, t_reservations[d].rnum))

        if clean_f[p].lower().startswith('lad'): # LAD STANDS FOR LIST ALL DEPARTURES
            outfile.write("Guests departing on {}:\n".format(clean_f[p][4:].strip()))
            print("Guests departing on {}:".format(clean_f[p][4:].strip()))
            for h in range(len(t_reservations)):
                if t_reservations[h].depart == clean_f[p][4:].strip():
                    outfile.write("   {} (room {})\n".format(t_reservations[h].gname, t_reservations[h].rnum))
                    print("   {} (room {})".format(t_reservations[h].gname, t_reservations[h].rnum))

        if clean_f[p].lower().startswith('lfb'): # LFB STANDS FOR LIST FREE SERVICE (EX: BEDROOMS)
            date = clean_f[p][4:].strip().split()
            outfile.write("Bedrooms free between {} to {}:\n".format(date[0], date[1]))
            print("Bedrooms free between {} to {}:".format(date[0], date[1]))
            date0M, date0D, date0Y = date[0].split("/")
            date1M, date1D, date1Y = date[1].split("/")
            date[0] = datetime.date(int(date0Y), int(date0M), int(date0D))
            date[1] = datetime.date(int(date1Y), int(date1M), int(date1D))
            reserved = set()
            free = set()
            notNeeded = set()
            for n in range(len(t_reservations)):
                dateArriveM, dateArriveD, dateArriveY = t_reservations[n].arrive.split("/")
                dateDepartM, dateDepartD, dateDepartY = t_reservations[n].depart.split("/")
                dateArrive = datetime.date(int(dateArriveY), int(dateArriveM), int(dateArriveD))
                dateDepart = datetime.date(int(dateDepartY), int(dateDepartM), int(dateDepartD))
                if not (date[0] <= dateArrive <= date[1]) and not (dateArrive <= date[0] <= dateDepart): # not in between
                    free.add(t_reservations[n].rnum)
                elif (date[0] == date[1] and not (dateArrive <= date[1] < dateDepart)): # the same date
                    free.add(t_reservations[n].rnum)
                if dateArrive < date[0] < dateDepart and t_reservations[n].rnum in free:
                    notNeeded.add(t_reservations[n].rnum)
                reserved.add(t_reservations[n].rnum)
            unreserved = set(r_nums) - reserved
            free |= unreserved
            free -= notNeeded
            for rnum in free:
                outfile.write("   {}\n".format(rnum))
                print("   {}".format(rnum))
    outfile.close()
    return

reservation()
