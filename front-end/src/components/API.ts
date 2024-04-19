import axios from 'axios';
import Phase from '../Phase';

class API {
    static endpoint = "http://127.0.0.1:8000";

    static async get(module: string, method: string) {
        const response = await axios.get(`${this.endpoint}/${module}/${method}`)
        return response.data;
    }

    static async post(module: string, method: string, data?: Object) {
        return await axios.post(`${this.endpoint}/${module}/${method}`, data);
    }

    static async getPhase(): Promise<{phase: Phase}> {
        return await this.get('viewer', 'phase/1');
    }

    static async getAllPlayers(): Promise<{players: string[]}> {
        return await this.get('viewer', 'players');
    }

    static async getAllSongs(): Promise<{songs: string[]}> {
        return await this.get('viewer', 'songs');
    }
}

export default API