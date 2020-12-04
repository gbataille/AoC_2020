import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


@dataclass
class Passport:
    byr: Optional[str] = None
    iyr: Optional[str] = None
    eyr: Optional[str] = None
    hgt: Optional[str] = None
    hcl: Optional[str] = None
    ecl: Optional[str] = None
    pid: Optional[str] = None
    cid: Optional[str] = None

    @property
    def valid(self) -> bool:
        return (self.byr_valid and self.iyr_valid and self.eyr_valid
                and self.hgt_valid and self.hcl_valid and self.ecl_valid
                and self.pid_valid)

    @property
    def byr_valid(self) -> bool:
        return self.byr is not None and int(self.byr) >= 1920 and int(
            self.byr) <= 2002

    @property
    def iyr_valid(self) -> bool:
        return self.iyr is not None and int(self.iyr) >= 2010 and int(
            self.iyr) <= 2020

    @property
    def eyr_valid(self) -> bool:
        return self.eyr is not None and int(self.eyr) >= 2020 and int(
            self.eyr) <= 2030

    @property
    def hgt_valid(self) -> bool:
        if self.hgt is None:
            return False

        if self.hgt[-2:] == 'cm':
            return int(self.hgt[:-2]) >= 150 and int(self.hgt[:-2]) <= 193
        elif self.hgt[-2:] == 'in':
            return int(self.hgt[:-2]) >= 59 and int(self.hgt[:-2]) <= 76
        else:
            return False

    @property
    def hcl_valid(self) -> bool:
        return self.hcl is not None and re.match(r'^#[0-9a-f]{6}$',
                                                 self.hcl) is not None

    @property
    def ecl_valid(self) -> bool:
        return self.ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    @property
    def pid_valid(self) -> bool:
        return self.pid is not None and re.match(r'^[0-9]{9}$',
                                                 self.pid) is not None


def parse_passports(input_str: str) -> List[Passport]:
    passports: List[Passport] = []
    passport: Passport = Passport()
    for line in input_str.split('\n'):
        if line == '':
            passports.append(passport)
            passport = Passport()
            continue

        fields = line.split(' ')
        for field in fields:
            key, value = field.split(':')
            setattr(passport, key, value)

    passports.append(passport)
    return passports


if __name__ == '__main__':
    input_str = get_input('4')
    passports = parse_passports(input_str)

    cnt = 0
    for passport in passports:
        if passport.valid:
            cnt += 1

    print(cnt)
