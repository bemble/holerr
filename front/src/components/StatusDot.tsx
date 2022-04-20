import classNames from "classnames";
import classes from "./StatusDot.module.scss";

export type Status = "success" | "error" | "pending";

type StatusDotProps = {
    status: Status
};

const StatusDot:React.FC<StatusDotProps> = ({status}) => {
    return <div className={classNames(classes.root, classes[status] )} />;
};

export default StatusDot;