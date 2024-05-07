import React, { useEffect, useState } from "react";
import API from "./API";
import Phase from "../Phase";

const AdminSong: React.FunctionComponent<{song: string}> = ({song}) => {
    return <li>{song}</li>
}

export default AdminSong;