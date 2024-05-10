import React from "react";
import { Song } from "../Models";

const AdminSong: React.FunctionComponent<{song: Song, updateSong: (song: Song) => void, mergeSource: Song | undefined, setMergeSource: (mergeSource: Song | undefined) => void, mergeSongs: () => void}> = ({song, updateSong, mergeSource, setMergeSource, mergeSongs}) => {
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setMergeSource(event.target.checked ? song : undefined);
    };

    return <li>
        <input type="text" onChange={(e) => updateSong({song_title: e.target.value, artist: song.artist})} value={song.song_title} />
            -
        <input type="text" onChange={(e) => updateSong({song_title: song.song_title, artist: e.target.value})} value={song.artist} />
        {mergeSource && mergeSource !== song ?
            <button onClick={mergeSongs}>Merge with {mergeSource.song_title}</button> :
            <input type="checkbox" onChange={handleChange} checked={mergeSource === song}/>
        }
    </li>
}

export default AdminSong;