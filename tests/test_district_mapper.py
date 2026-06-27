from etl.utils.district_mapper import DistrictMapper

mapper = DistrictMapper()

print(
    mapper.get_district_id("Lalitpur")
)