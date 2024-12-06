import ntplib
import datetime


class SyncTime:
    def synchronize(self, serv: str):
        self.offset = datetime.timedelta(seconds=0)

        print("synchronizing to", serv)
        c = ntplib.NTPClient()
        resp = c.request(serv)
        self.offset = datetime.timedelta(seconds=resp.offset)
        print(f"time: {self.now()} (offset: {self.offset})")

    def now(self):
        curr_local_time = datetime.datetime.now(datetime.timezone.utc)
        return curr_local_time + self.offset


def main():
    s = SyncTime()
    s.synchronize("pool.ntp.org")
    print("local time: ", datetime.datetime.now())
    print("synced time: ", s.now())


if __name__ == "__main__":
    main()
