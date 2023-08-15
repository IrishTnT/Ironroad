import { writable } from 'svelte/store';
import type { PageServerLoad, Actions} from './$types';
import axios from 'axios';

export const load = (async () => {
    const urlBase = "https://api.irishtnt.com/trackengine/";
    
    // Get all stations
    const { stations } = await (await axios.post(urlBase + "stations")).data;

    return {
        stations: stations,
    };
}) satisfies PageServerLoad;

export const actions = {
    default: async ({ cookies, request }) => {
        const urlBase = "https://api.irishtnt.com/trackengine/stations/code";

        let reqData = await request.formData()
        let code = reqData.get("stationCode");
        let time = reqData.get("time");

        if (time == "") {
            time = "90";
        }

        const { data } = await axios.post(urlBase + "/" + code + "/" + time);

        // Remove train code, scheduled departure, direction, train type and location type
        data.station.trains.forEach((train: { trainCode: any; scheduledArrival: any; lastLocation: any; status: any; scheduledDeparture: any; direction: any; trainType: any; locationType: any; originTime: any; destinationTime: any; dueIn: string; late: string; }) => {
            delete train.trainCode;
            delete train.scheduledArrival;
            delete train.lastLocation;
            delete train.status;
            delete train.scheduledDeparture;
            delete train.direction;
            delete train.trainType;
            delete train.locationType;
            delete train.originTime;
            delete train.destinationTime;
            train.dueIn = train.dueIn + " mins";
            train.late = train.late + " mins";
        });

        return {
            success: true,
            trains : data.station.trains
        };
    }
} satisfies Actions;