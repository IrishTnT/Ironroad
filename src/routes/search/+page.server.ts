import type { PageServerLoad } from './$types';
import axios from 'axios';
import convert from 'xml-js';

export const load = (async () => {
    // Get Station information
    const { stationdata } = await axios.get('http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML');
    const json = convert.xml2json(stationdata, { compact: true, spaces: 4 });
    const stations = JSON.parse(json).ArrayOfObjStation.objStation;
    const stationNames = stations.map((station: any) => station.StationDesc._text);
    const stationCodes = stations.map((station: any) => station.StationCode._text);
    // Find and remove repeats
    const uniqueStationNames = stationNames.filter((item: any, index: any) => stationNames.indexOf(item) === index);
    // Manually remove "PARK WEST"
    const parkWestIndex = uniqueStationNames.indexOf('PARK WEST');
    uniqueStationNames.splice(parkWestIndex, 1);

    // Get train information
    const { traindata } = await axios.get('http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML');
    const trainJson = convert.xml2json(traindata, { compact: true, spaces: 4 });
    const trains = JSON.parse(trainJson).ArrayOfObjTrainPositions.objTrainPositions;
    const rawTrainData = trains.map((train: any) => train.PublicMessage._text);

    // Public Message follows the following structure:
    // "[ID]\n[Departure Time] - [Origin] to [Destination]([time] mins late/early)\n[Status]"
    // We want to extract the following:
    // [Departure Time], [Origin], [Destination], time (mins late/early), [Status]
    const trainData = rawTrainData.map((train: any) => {
        const trainData = train.split('\n');
        const trainId = trainData[0];
        const trainDepartureTime = trainData[1].split(' - ')[0];
        const trainOrigin = trainData[1].split(' - ')[1].split(' to ')[0];
        const trainDestination = trainData[1].split(' - ')[1].split(' to ')[1].split('(')[0];
        const trainTime = trainData[1].split(' - ')[1].split(' to ')[1].split('(')[1].split(')')[0];
        const trainStatus = trainData[2];
    });

    return {
        stations: uniqueStationNames
    };
}) satisfies PageServerLoad;