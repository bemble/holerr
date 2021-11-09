import {Card, CardContent, Grid, IconButton, makeStyles,} from "@material-ui/core";
import DeleteIcon from "@material-ui/icons/DeleteOutlined";
import {useDispatch} from "react-redux";
import {Download} from "../../models/downloads.type";
import {DEFAULT_STATUS_CONFIG, downloadStatusConfig} from "../../models/downloads.utils";
import {deleteDownload} from "../../store/downloads/downloads.thunk";
import DownloadItemChips from "./DownloadItemChips";
import StateProgress from "../../components/StateProgress";
import {blue} from "@material-ui/core/colors";
import {FunctionComponent} from "react";

type DownloadItemProps = {
    item: Download;
};

const useStyles = makeStyles(({spacing}) => ({
    content: {
        padding: `${spacing(2)}px !important`
    },
    status: {
        paddingRight: spacing(2)
    },
    title: {
        flex: 1,
        wordBreak: "break-all",
        color: blue[900]
    },
}));

const DownloadItem: FunctionComponent<DownloadItemProps> = ({item}) => {
    const {status, step} = downloadStatusConfig.get(item.status) || DEFAULT_STATUS_CONFIG;
    const dispatch = useDispatch();
    const classes = useStyles();

    const handleDeleteClick = () => {
        dispatch(deleteDownload(item.id));
    };

    const torrentProgress = item.torrent_info?.progress || 0;
    const downloadProgress = item.download_info?.progress || 0;

    return <Card elevation={1}>
        <CardContent className={classes.content} >
            <Grid container alignItems="center">
                <Grid item className={classes.status}>
                    <StateProgress torrentProgress={torrentProgress} downloadProgress={downloadProgress} step={step}
                                   status={status}/>
                </Grid>
                <Grid item className={classes.title}>
                    {item.title}
                </Grid>
                <Grid item>
                    <IconButton onClick={handleDeleteClick} size="small"><DeleteIcon/></IconButton>
                </Grid>
            </Grid>
            <DownloadItemChips item={item}/>
        </CardContent>
    </Card>;
};

export default DownloadItem;
