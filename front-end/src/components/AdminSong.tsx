import React, { useEffect, useState } from "react";
import API from "./API";
import Phase from "../Phase";
import { Song } from "../Models";

const AdminSong: React.FunctionComponent<{song: Song}> = ({song}) => {
    return <li>{song.song_title} - {song.artist}</li>
}

export default AdminSong;